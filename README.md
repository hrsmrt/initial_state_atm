# 理想化実験の初期大気場生成コード

気象モデルで行う理想化実験のための初期大気場を生成するコードです。修士課程における研究で使用しているものです。

- 2025.4  コード公開
- 2025.10 FortranからPythonへ移行中

## 使用方法

- 作業ディレクトリを作成する
- setting/params.pyを作業ディレクトリにコピーし、編集する
- 各自で定めた作業ディレクトリで、run_all.pyを実行すると、データおよび図が生成される
  - 個別に実行も可。例えばprogram/mkdata/cartesian.pyを実行すると、データのみ生成される

## 実行ファイルの概要

- `cartesian.py`
  - 直交座標系の場を生成

- `utils/params.py`
  - ここで変数の設定を記述

- `Makefile`
  - Fortranプログラムをコンパイル(旧ver)

- `mkfig/`
  - 描画プログラムファイルを入れるフォルダ

## 注意事項

- 本プログラムは、Plane-NICAM(Ohno and Satoh 2015, Satoh 2014)で熱帯低気圧のシミュレーションを行うために作成しています。
- 周期境界条件の領域モデルにおいてPoint-downscaling法(Nolan, 2011)を用いることを想定しています。

## 渦について

- 生成される渦は軸対称であり、静水圧平衡及び傾度風平衡を満たします。

- `vortex`
  - 軸対称な渦のrz分布を計算するプログラム
  - 入力: 接線風速分布に関するパラメータ
  - 出力: 接線風速、圧力、気温場
  - 計算手法はNolan et al. (2001)を参考にした

- `wind_profile`
  - 風速の鉛直分布を出力するプログラム
  - 渦形状はNolan(2007)、stern and Nolan(2011)、Nolan et al. (2024)を参考にした

## 参考文献

- Ohno, T., & Satoh, M. (2015). On the warm core of a tropical cyclone formed near the tropopause. Journal of the Atmospheric Sciences, 72(2), 551-571.
- Satoh, M., Tomita, H., Yashiro, H., Miura, H., Kodama, C., Seiki, T., ... & Kubokawa, H. (2014). The non-hydrostatic icosahedral atmospheric model: Description and development. Progress in Earth and Planetary Science, 1, 1-32.
- Nolan, D. S., Montgomery, M. T., & Grasso, L. D. (2001). The wavenumber-one instability and trochoidal motion of hurricane-like vortices. Journal of the atmospheric sciences, 58(21), 3243-3270.
- Nolan, D. S., Rappin, E. D., & Emanuel, K. A. (2007). Tropical cyclogenesis sensitivity to environmental parameters in radiative–convective equilibrium. Quarterly Journal of the Royal Meteorological Society: A journal of the atmospheric sciences, applied meteorology and physical oceanography, 133(629), 2085-2107.
- Nolan, D. S. (2011). Evaluating environmental favorableness for tropical cyclone development with the method of point‐downscaling. Journal of Advances in Modeling Earth Systems, 3(3).
- Nolan, D. S., Nebylitsa, S., McNoldy, B. D., & Majumdar, S. J. (2024). Modulation of tropical cyclone rapid intensification by mesoscale asymmetries. Quarterly Journal of the Royal Meteorological Society, 150(758), 388-415.
- Stern, D. P., & Nolan, D. S. (2011). On the vertical decay rate of the maximum tangential winds in tropical cyclones. Journal of the atmospheric sciences, 68(9), 2073-2094.
