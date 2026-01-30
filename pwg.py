import os
import sys
import random
import const

def pwg(digit:int=8,num:int=10,charactor_type=const.character_type.ALPHABETS_NUMBERS_SIGNS,signs:str='_?',first_charactor_alphabets:bool=False) -> list[str]:

  # 生成対象文字の絞り込み
  charactors: list[str] = [const.ALPHABETS_L, const.ALPHABETS_U]
  match charactor_type:
    case const.character_type.ALPHABETS_SIGNS.value:
      charactors.append(signs)
    case const.character_type.ALPHABETS_NUMBERS.value:
      charactors.append(const.NUMBERS)
    case const.character_type.ALPHABETS_NUMBERS_SIGNS.value:
      charactors.append(const.NUMBERS)
      charactors.append(signs)
  
  # 生成していく
  passwords: list[str] = []
  for _ in range(num):
    password: str = ''
    biases: list[int] = []
    for _ in range(len(charactors)):
      biases.append(0)
    for i in range(digit):
      target_charactors_index = least_charactors_index(biases)
      if i == 0 and first_charactor_alphabets:
        target_charactors_index = random.randrange(2)
      target_charactors = charactors[target_charactors_index]
      charactor = target_charactors[random.randint(0, len(target_charactors)-1)]
      password += charactor
      biases[target_charactors_index] += 1
    passwords.append(password)

  return passwords

def least_charactors_index(biases:list[int]) -> int:
  idxs:list[int] = []
  min_value:int = 65535
  for i in range(len(biases)):
    if biases[i] < min_value:
      idxs = [i]
      min_value = biases[i]
    elif biases[i] == min_value:
      idxs.append(i)
  idx:int = idxs[0]
  if len(idxs) > 1:
    idx = idxs[random.randint(0, len(idxs)-1)]
  return idx

if __name__ == "__main__":
  passwords: list[str] = pwg()
  for password in passwords:
    print(password)
