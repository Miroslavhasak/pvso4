PVSO 4. Zadanie
**Znenie zadania**

Ciel’om zadania, je oboznámit’ sa s pracou s mraˇcnom bodov (point cloud) a segmentácia ob
jektov v priestore. Študent si vyskúšavytvorenievlastnéhomraˇcnabodovaaplikáciumetódna
 získanie segmentovaného priestoru. Použitie externých knižníc ako open3d, sklearn, opencv,
 a iných je dovolené a odporúˇ cané.
 Zadanie je dokopy za 25b.apozostávazviacerých úloh:

 **Úlohy:**
 1. Vytvorenie mraˇ cna bodov pomocou Kinect v2 pre testovanie. Nájdite online na webe
 mraˇ cno bodov popisujúce väˇcší priestor (väˇcší objem dát aspoˇ n 4 x 4 metre) pre testo
vanie algoritmov a naˇ cítajte mraˇcno dostupného datasetu [2 b.].

2. Pomocou knižnice (open3d- python) naˇcítate vytvorené mraˇcno bodov a zobrazíte. [2
 b.].

3. Mraˇ cnábodovoˇ cistiteodokrajovýchbodov.Pretutoúlohujevhodnepoužit’algoritmus
 RANSAC[5b.].

4. Segmentujete priestor do klastrov pomocou vhodne zvolených algoritmov (K-means,
 DBSCAN, BIRCH, Gausian mixture, mean shift ...). Treba si zvolit’ aspoˇ n 2 algoritmy a
 porovnat’ ich výsledky [5+5 b.].

5. Detailne vysvetlite fungovanie zvolených algoritmov. [4 b.] (Ked’že neimplementujete
 konkrétny algoritmus ale používate funkcie tretích strán je potrebné rozumiet’ aj ako sú
 funkcie implementované)

6. Vytvorte dokumentáciu zadania:
 • popisimplementovanýchalgoritmov,
 • graficképorovnanie výstupov,
 • vysvetlite rozdiel v kvalite výstupov pre rozdielne typy algortimov.
  [2 b.].