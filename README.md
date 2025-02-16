# PyChess - Chess implementation in Python

> The codebase is pretty bad, and could do with a rewrite.
>
> When I end up doing a rewrite is unclear however
> it'll probably be in a few years


Chess program in Python (including an AI opponent)

![Image of PyChess](./preview/image.png)


To download this to your computer, there are two methods:
> People with `git` installed can use `git clone https://github.com/commandcontrolQ/pychess-tf`.
> 
> If you do not have git, you can click on the green 'Code' button and then select `Download ZIP`,
> or you can use this link: [https://tinyurl.com/pychessgit](https://tinyurl.com/3tzh2567)

## Troubleshooting

```
Traceback (most recent call last):
  File "C:\foo\bar\pychess.py", line 253, in <module>
    import pygame
ModuleNotFoundError: No module named 'pygame'
```
You will get this error if you do not have pygame installed.
To install pygame, run the command `pip install pygame`.
> If that command does not run, try using `py -m pip install pygame`, `python -m pip install pygame`, or `python310 -m pip install pygame`.
>
> If you already have installed pygame, then you likely have more than one installation of Python, and they are conflicting. **Make sure that you run the program using the version of Python that pygame was installed onto!**

This work is licensed under CC BY-NC-SA 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/.

<img src="https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png" alt="" width="88" height="31">
