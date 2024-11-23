# Diffsinger_tools

## 这是一个适用于diffsinger的数据集制作流程的工具仓库。

### htk2cdd_ph_numcsv.py

可以创建transcriptions.csv的同时添加ph_hum

```
python htk2cdd_ph_numcsv.py （HTK标注路径） -o -d
```

### add_ph_num_plus

可以添加多段式（如英文，汉语三段式）的ph_hum,并且优化了多线程，加入了进度条
```
python add_ph_num_plus.py -c -d 
```

### dictionary_to_dsdict_plus

可以处理多段式词典，直接生成dsdict

```
python dictionary_to_dsdict_plus.py (词典) -o 
```
