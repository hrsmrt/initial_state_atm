# 渦生成

- 渦を生成するプログラムです。台風の理想化実験を行うことを目的としています。
- Plane-NICAM(Ohno and Satoh 2015, Satoh 2014)でシミュレーションを行うことを想定しています。
- 周期境界条件の領域モデルにおいてPoint-downscaling法(Nolan, 2011)を用いることを想定しています。
- 生成される渦は軸対称であり、静水圧平衡及び傾度風平衡を満たします。

## 使用手順

- `utils/params.py`を編集
- `make`: fortranプログラムのコンパイル
- `make run`: データ及び基本的な図の生成

## 実行ファイルの概要

- `vortex`
  - 軸対称な渦のrz分布を計算するプログラム
  - 入力: 接線風速分布に関するパラメータ
  - 出力: 接線風速、圧力、気温場
  - 計算手法はNolan et al. (2001)を参考にした

- `wind_profile`
  - 風速の鉛直分布を出力するプログラム
  - 渦形状はNolan(2007)、stern and Nolan(2011)、Nolan et al. (2024)を参考にした

- `cartesian`
  - 直交座標系の場を作成

- `setting.py`
  - ここで変数の設定を記述

- `write_nml.py`
  - `setting.py`で設定した内容をnmlファイルに書き出す

- `Makefile`
  - Fortranプログラムをコンパイル

- `mkfig/`
  - 描画プログラムファイルを入れるフォルダ

## 参考文献

- Ohno, T., & Satoh, M. (2015). On the warm core of a tropical cyclone formed near the tropopause. Journal of the Atmospheric Sciences, 72(2), 551-571.
- Satoh, M., Tomita, H., Yashiro, H., Miura, H., Kodama, C., Seiki, T., ... & Kubokawa, H. (2014). The non-hydrostatic icosahedral atmospheric model: Description and development. Progress in Earth and Planetary Science, 1, 1-32.
- Nolan, D. S., Montgomery, M. T., & Grasso, L. D. (2001). The wavenumber-one instability and trochoidal motion of hurricane-like vortices. Journal of the atmospheric sciences, 58(21), 3243-3270.
- Nolan, D. S., Rappin, E. D., & Emanuel, K. A. (2007). Tropical cyclogenesis sensitivity to environmental parameters in radiative–convective equilibrium. Quarterly Journal of the Royal Meteorological Society: A journal of the atmospheric sciences, applied meteorology and physical oceanography, 133(629), 2085-2107.
- Nolan, D. S. (2011). Evaluating environmental favorableness for tropical cyclone development with the method of point‐downscaling. Journal of Advances in Modeling Earth Systems, 3(3).
- Nolan, D. S., Nebylitsa, S., McNoldy, B. D., & Majumdar, S. J. (2024). Modulation of tropical cyclone rapid intensification by mesoscale asymmetries. Quarterly Journal of the Royal Meteorological Society, 150(758), 388-415.
- Stern, D. P., & Nolan, D. S. (2011). On the vertical decay rate of the maximum tangential winds in tropical cyclones. Journal of the atmospheric sciences, 68(9), 2073-2094.
