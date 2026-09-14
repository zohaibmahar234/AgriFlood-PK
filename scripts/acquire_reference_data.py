"""Print verified reference sources for the Khairpur District 2022 case study.
Downloads are intentionally not automated because source packaging/licensing can change.
"""
refs=[
 ('UNOSAT Sindh flood assessment as of 15 Aug 2022','https://unosat.org/static/unosat_filesystem/3335/UNOSAT_A3_Natural_Portrait_FL20220808PAK_SindhProvince_Pakistan_15Aug2022.pdf'),
 ('UNOSAT flood evolution assessment — Khairpur District imagery, 9 Sep 2022','https://unosat.org/static/unosat_filesystem/3350/Preliminary%20satellite-derived%20flood%20evolution%20assessment%20-%209%20September%202022.pdf'),
 ('UNOSAT Product 3352 — Pakistan flood assessment','https://unosat.org/products/3352'),
 ('UNOSAT weekly update — late Dec 2022 recession context','https://unosat.org/static/unosat_filesystem/3470/UNOSAT_Preliminary_Assessment_Report_FL20221121PAK_Pakistan_WeeklyUpdate_20230103.pdf')]
for name,url in refs: print(f'{name}: {url}')
print('Download any offered vector/reference package only after checking its licence/terms; preserve source metadata and place external files under data/reference/external/.')
