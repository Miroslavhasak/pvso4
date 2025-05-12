# PVSO 4. Zadanie

**Znenie zadania**

Cieľom zadania, je oboznámit’ sa s pracou s mračnom bodov (point cloud) a segmentácia ob
jektov v priestore. Študent si vyskúša vytvorenie vlastného mračna bodov a aplikáciu metód na
 získanie segmentovaného priestoru. Použitie externých knižníc ako open3d, sklearn, opencv,
 a iných je dovolené a odporúčané.
 Zadanie je dokopy za 25b.a pozostáva z viacerých úloh:

 ### Úlohy:
 1. Vytvorenie mračna bodov pomocou Kinect v2 pre testovanie. Nájdite online na webe
 mračno bodov popisujúce väčší priestor (väčší objem dát aspoň 4 x 4 metre) pre testo
vanie algoritmov a načítajte mračno dostupného datasetu [2 b.].

2. Pomocou knižnice (open3d- python) načítate vytvorené mračno bodov a zobrazíte. [2
 b.].

3. Mračná bodov očistite od okrajových bodov.Pre tuto úlohu je vhodné použit’ algoritmus
 RANSAC[5b.].

4. Segmentujete priestor do klastrov pomocou vhodne zvolených algoritmov (K-means,
 DBSCAN, BIRCH, Gausian mixture, mean shift ...). Treba si zvolit’ aspoň 2 algoritmy a
 porovnat’ ich výsledky [5+5 b.].

5. Detailne vysvetlite fungovanie zvolených algoritmov. [4 b.] (Keďže neimplementujete
 konkrétny algoritmus ale používate funkcie tretích strán je potrebné rozumieť aj ako sú
 funkcie implementované)

6. Vytvorte dokumentáciu zadania: [2 b.].

 • popis implementovaných algoritmov,

 • grafické porovnanie výstupov,

 • vysvetlite rozdiel v kvalite výstupov pre rozdielne typy algortimov.

# Dokumentácia 

V zadaní sme použili 2 algoritmy a to K-means DBSCAN.

### K-means

Tento algoritmus funguje tak ze si vytvoríme k klustrov ku ktorým priradíme najbližšie 
body pomocou vzdialenosti následne najdeme stred klustrov a znova odmeráme vzdialenosti 
každého bodu od klustrov.

### DBSCAN

DBSCAN je hustotne založený algoritmus, ktorý vytvára klastre na základe hustoty bodov 
v priestore. Pre každý bod vyhľadá okolie v určitej vzdialenosti. Ak má okolie aspoň 
min_points bodov, považuje sa za jadrový bod a vytvorí nový klaster, ku ktorému sa 
pridávajú všetky husté susedné body. Body, ktoré nepatria do žiadneho klastru, 
sa označia ako šum. Algoritmus dokáže nájsť arbitrárne tvarované klastre a zároveň 
identifikovať odľahlé body bez potreby určovať počet klastrov vopred.

Po aplikovaní každého algoritmu sa výsledné klastre vizualizujú pomocou Open3D:

K-means:

Každý klaster je farebne rozlíšený.

Výstupné okno: "K-means clustering"

DBSCAN:

Vizualizácia zhlukov s odstráneným šumom.

Výstupné okno: "Segmented space"
