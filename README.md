# RoomBooking

1. 为什么把房间写成类？
    -1-因为房间信息不只有静态属性，还有很多对房间信息的操作，例如预定房间，更新房间状态信息
    -2-便于管理，可以对每一个房间进行快速的单独操作，互不干扰
2. 如何判断预定时间与现存已预定时间冲突？
    - 排除所有冲突的时间段
    - 起始时间和终止时间均不要落在已存在时间段中
3. 如何让每次进入程序的时候都是上一次结束的状态？
    -通过将对象实例化，保存到文件中，每次程序结束时进行保存，每次开始时从文件中读取对象
     -1-登陆验证token：注册时，数据库最好不存密码以免泄露，sh256(a kind of hash algorithm), store a str generated from user name ands password, 每次登录进行比对验证身份
     -2-临时授权token：每次登陆之后，serve生成一个带有时效性的token，发送给client，每次client发送操作命令要带着token来验证身份。 serve通过token来识别用户身份和权限。
4. 如何进行页面覆盖和返回
   - 页面的切换实际上是表格数据以及按钮的切换。
5. 在遍历字典时删除元素会产生报错

报错代码如下

```python
for room_id,room in RoomData.items():
    if room.Capacity > int(conditions['CapacityMax']):
        RoomData.pop(room_id)
```

报错如下：

```
dictionary changed size during iteration
```

解决方案：迭代字典`key`值组成的`list`而非字典本身，从而解决这个问题：

```
for room_id in list(RoomData.keys()):
    if RoomData[room_id].Capacity < int(conditions['CapacityMin']):
        RoomData.pop(room_id)
```





- 部分单元格自动填写及锁定
- 日期部分使用选中输入
- 看到他人订阅时名字匿名显示
