(* sync-wb-nb.wls — canonical .wb -> .nb cell sync.
   Usage (run from anywhere; set defaultWb/defaultNb below or pass paths as trailing args):
     wolframscript -file sync-wb-nb.wls verify    "<snippet>"
     wolframscript -file sync-wb-nb.wls stability "<snippet>"
     wolframscript -file sync-wb-nb.wls replace   "<wbSnippet>" ["<nbOldSnippet>"]
     wolframscript -file sync-wb-nb.wls insert    "<wbSnippet>" "<nbAnchorSnippet>"
     ... [optional trailing args: <wbPath> <nbPath>]
   Snippets MUST be single tokens (symbol names like "myFunction"): in box structures,
   "myFunc[x_" never matches because myFunc, [, x_ are separate strings.
   Modes:
     verify    - assert the .nb cell matching <snippet> parses === the .wb cell. No write.
     stability - assert the .wb cell code survives code->boxes->code with ===. No write.
     replace   - replace the unique .nb cell matching <nbOldSnippet> (default: <wbSnippet>)
                 by the .wb cell matching <wbSnippet>. Backs up, verifies, aborts on any
                 ambiguity or mismatch.
     insert    - insert the .wb cell after the unique .nb cell matching <nbAnchorSnippet>.
   Exit code 0 = success/PASS, 1 = failure (file restored from backup on failed write). *)

(* ── Project defaults ──────────────────────────────────────────────────────
   Set these to your file pair so you can call the script without trailing
   args. Leave as "" to require explicit paths every time.              *)
defaultWb = "";   (* e.g. "/abs/path/to/project/numerics/mynotebook.wb" *)
defaultNb = "";   (* e.g. "/abs/path/to/project/numerics/mynotebook.nb" *)
(* ────────────────────────────────────────────────────────────────────────── *)

args = Rest[$ScriptCommandLine];
If[Length[args] < 2, Print["FAIL: need <mode> <snippet> [...]"]; Exit[1]];
{mode, snip1} = args[[1 ;; 2]];
snip2 = If[Length[args] >= 3 && ! StringContainsQ[args[[3]], "/"], args[[3]], snip1];
paths = Select[args, StringContainsQ[#, "/"] &];
die[msg_] := (Print["FAIL: ", msg]; Exit[1]);
wbfile = If[Length[paths] >= 1, paths[[1]],
   If[defaultWb =!= "", defaultWb, die["no .wb path — pass as trailing arg or set defaultWb above"]]];
nbfile = If[Length[paths] >= 2, paths[[2]],
   If[defaultNb =!= "", defaultNb, die["no .nb path — pass as trailing arg or set defaultNb above"]]];

str[b_] := ToString[b, InputForm, PageWidth -> Infinity];

wb = Quiet[Import[wbfile, "RawJSON"]];
If[Head[wb] =!= Association, die["cannot read .wb " <> wbfile]];
wbMatches = Select[wb["cells"], #["kind"] === 2 && StringContainsQ[#["value"], snip1] &];
If[Length[wbMatches] =!= 1,
  die["wb cells matching '" <> snip1 <> "': " <> ToString[Length[wbMatches]] <> " (need 1)"]];
code = wbMatches[[1]]["value"];

(* stability: code -> boxes -> code must be the identity on the parsed expression *)
e1 = ToExpression[code, StandardForm, HoldComplete];
boxes = ToExpression[code, StandardForm,
   Function[e, MakeBoxes[e, StandardForm], HoldAllComplete]];
e2 = ToExpression[boxes, StandardForm, HoldComplete];
stableQ = (e1 === e2);
If[mode === "stability",
  If[stableQ, Print["PASS: stable"]; Exit[0],
   die["NOT box-round-trip stable; rewrite the source (e.g. product-numerator fraction a*b/c -> assign numerator to a local; see SKILL.md)"]]];
If[! stableQ,
  die["wb code is not box-round-trip stable; run stability mode and fix the source first"]];

nb = Import[nbfile];
If[Head[nb] =!= Notebook, die["cannot read .nb " <> nbfile]];
nCells = Count[nb, _Cell, Infinity];
allPos = Position[nb, Cell[BoxData[_], "Input", ___]];
findPos[snip_] := Select[allPos, StringContainsQ[str[Extract[nb, #][[1, 1]]], snip] &];

If[mode === "verify",
  pos = findPos[snip1];
  If[Length[pos] =!= 1, die["nb cells matching '" <> snip1 <> "': " <> ToString[Length[pos]]]];
  exprNb = ToExpression[Extract[nb, pos[[1]]][[1, 1]], StandardForm, HoldComplete];
  If[exprNb === e1, Print["PASS: nb cell === wb cell"]; Exit[0],
   die["nb cell differs from wb cell"]]];

(* write modes: back up first *)
backup = "/tmp/sync-wb-nb-backup-" <> ToString[AbsoluteTime[] // Round] <> ".nb";
CopyFile[nbfile, backup];
Print["backup: ", backup];
newCell = Cell[BoxData[boxes], "Input", ExpressionUUID -> CreateUUID[]];

newnb = Which[
  mode === "replace",
  pos = findPos[snip2];
  If[Length[pos] =!= 1, die["nb target cells matching '" <> snip2 <> "': " <> ToString[Length[pos]] <> " (need 1)"]];
  ReplacePart[nb, pos[[1]] -> newCell],
  mode === "insert",
  pos = findPos[snip2];
  If[Length[pos] =!= 1, die["nb anchor cells matching '" <> snip2 <> "': " <> ToString[Length[pos]] <> " (need 1)"]];
  anchor = Extract[nb, pos[[1]]];
  nb /. (c : Cell[___, ExpressionUUID -> (anchor /. Cell[___, ExpressionUUID -> u_, ___] :> u), ___]) :> Sequence[c, newCell],
  True, die["unknown mode " <> mode]];

expected = nCells + If[mode === "insert", 1, 0];
If[Count[newnb, _Cell, Infinity] =!= expected,
  die["cell count wrong after " <> mode <> "; nothing written"]];
Export[nbfile, newnb];

(* verify the write *)
nb2 = Import[nbfile];
pos2 = Select[Position[nb2, Cell[BoxData[_], "Input", ___]],
   StringContainsQ[str[Extract[nb2, #][[1, 1]]], snip1] &];
ok = Length[pos2] >= 1 &&
   AnyTrue[pos2, ToExpression[Extract[nb2, #][[1, 1]], StandardForm, HoldComplete] === e1 &] &&
   Head[nb2] === Notebook;
If[ok, Print["PASS: ", mode, " verified (cells: ", Count[nb2, _Cell, Infinity], ")"]; Exit[0],
  CopyFile[backup, nbfile, OverwriteTarget -> True];
  die["post-write verification failed; .nb RESTORED from backup"]];
