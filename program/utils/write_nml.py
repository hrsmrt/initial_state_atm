import os
from params import settings

def main():
    os.makedirs("config", exist_ok=True)
    generate_nml()
    print("Namelist file written successfully.")

def generate_nml():
    write_namelist("config/param.nml", settings)
    e_to_d("config/param.nml")

def write_namelist(nml_path, namelist_dict):
    """与えられた辞書からFortran用namelistファイルを出力する。"""
    with open(nml_path, 'w') as f:
        for group_name, variables in namelist_dict.items():
            f.write(f"&{group_name}\n")
            for var, val in variables.items():
                # 値の型に応じてフォーマット
                if isinstance(val, str):
                    f.write(f"  {var} = '{val}'\n")
                elif isinstance(val, bool):
                    f.write(f"  {var} = {'.true.' if val else '.false.'}\n")
                else:
                    f.write(f"  {var} = {val}\n")
            f.write("/\n\n")

def e_to_d(filepath):
    # e → d に置換して倍精度に見せかける（Fortranで正しく読めるように）
    with open(filepath, 'r') as f:
        text = f.read()

    # Fortranの浮動小数点リテラルのみに適用するように工夫
    import re
    text = re.sub(r'([-+]?\d+\.\d+(?:[eE][-+]?\d+))', lambda m: m.group(1).replace('e', 'd').replace('E', 'D'), text)

    with open(filepath, 'w') as f:
        f.write(text)

if __name__ == "__main__":
    main()
