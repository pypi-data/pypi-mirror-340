# workflow

# Motivation
+ fire的ui反人类, typer的很优雅, 但是感觉完全为了CLI app服务, 并不想兼容一般函数, 要设置函数参数的默认值为各种typer自己的类型, 也不好
+ So, 拟开发一个相对简单, 但是兼容性好的CLI app wrapper: easyarg
+ 初始阶段就是针对python, 未来或许可以搞成跨语言的东东...
+ Slogan: Less is More, Simple is Better!


# WorkFlow

## easyarg-improve | @2025-04 ~
*@2025-04-10 18:24:42*
### bugfix: default value of bool arguments
+ See `utest/app.py:vtks2ver`
+ 发现函数定义里明明设置了`binary: bool = True`, easyarg里还是默认为False
+ <font color="green">√</font> 好吧, 发现是对于`bool`类型的参数, 调用`add_argument`的时候忘记传参`default=default`了...mdzz<sub style="color:gray">@18:32:57</sub>
### bugfix: wrong place of `--no-arg` for multiple bool args
+ See `utest/app.py:vtks2ver`
+ 发现如果有两个bool参数, `--no-arg`的形式, 全都挤在一个arg里了...
+ 不过这是不是 **libargparse.py** 的锅啊, 啊?
	+ 果然, 是actions的顺序问题....
	+ See **G::rdee-python/Export/libargparse.py # sort_actions**

## easyarg-init | @2024-11 ~ 2025-02
*@2025-02-26 20:06:20*
+ 完成了对argumentparser的分离, 很好, 现在那个放在rdee-python/Export上去

*@2025-02-25 14:30:33*
+ 这几天进行了巨大优化, 主要是help信息的优化, 以及command支持更多参数定制化的优化, CLI-executor从直接执行module改成了`pyfexe`, 然后孵化了一个新的idea, 就是把自定的argumentparser独立出去, 因为其他地方理论上也可以用, yes!

*@2024-11-28 22:45:31*
+ 加一个对任意generic参数函数包装命令行接口的功能, 仍然强需求显示类型声明

*@2024-11-23 14:25:27*
+ ok, 实现了一版极简的, 完全依托于标准argparse的东西
+ argument仅支持python的intrinsic type: int, float, str & bool
+ 测试似乎是可用的了, 然后想想后续的更新方向:
    + 1. customized help information, 这个可以参考typer的, 人家那个确实挺好看
    + 2. 实现无接触式的直接执行, 即不需要什么decorator之类的, 直接强制执行你这个函数

*@2024-11-22 22:18:22*
+ 先找GPT写一版简单的, 然后再改吧...