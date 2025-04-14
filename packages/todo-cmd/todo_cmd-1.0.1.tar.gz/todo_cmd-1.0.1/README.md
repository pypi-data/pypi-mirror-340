```
                                                   __
 __________  ____  ____        _________ ___  ____/ /
/_  __/ __ \/ __ \/ __ \______/ ___/ __ `__ \/ __  / 
 / / / /_/ / /_/ / /_/ /_____/ /__/ / / / / / /_/ /  
/_/  \____/_____/\____/      \___/_/ /_/ /_/\__,_/   
                         
```

欢迎使用 **todo-cmd**，这是一个简单的工具，帮助您在命令行中轻松管理代办、记录完成事项。**[中文文档在这里](./README_zh.md)**

Welcome to the **todo-cmd**!
This is a simple tool to help you manage your tasks.

![snap](./docs/todo_ls.png)


## 1. Features

1. Commandline interface, easy to use
2. Simple and beautiful TUI
3. Support multiple status: `todo`, `done`, `expired`, `discarded`
4. Support task priority: `p0`, `p1`, `p2`, `p3`

## 2. Installation

### 2.1 👍 Use `uv` or `pipx`

```bash
# if you don't have uv
pip3 install uv

# Use uv
uv tool install todo-cmd

# or use pipx
pipx install todo-cmd
```

uninstall

```bash
# Use uv
uv tool uninstall todo-cmd

# Use pipx
pipx uninstall todo-cmd
```

### 2.2 Install from source

```shell
git clone https://github.com/paperplane110/todo_cmd.git
cd todo_cmd
pip3 install .
```

## 3. Usage

### Add a todo task

```bash
todo add ${task}

# or use shortcut
todo a ${task}

# with deadline
todo add ${task} --deadline ${YYYYMMdd}
todo add ${task} -ddl ${YYYYMMdd}
```

### Add a finished task

```shell
todo log ${task}

# or use shortcut
todo l ${task}
```

### List tasks

List all tasks

```shell
todo ls
```
```txt
┏━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ id ┃ Status ┃ Task                                 ┃  Deadline  ┃ Finish Date ┃
┡━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 10 │  expr  │ Apply a card for my electric-bike    │ 2024-11-10 │      /      │
├────┼────────┼──────────────────────────────────────┼────────────┼─────────────┤
│ 9  │  todo  │ ask Liuke about perf monitor scripts │ 2024-11-13 │      /      │
├────┼────────┼──────────────────────────────────────┼────────────┼─────────────┤
│ 8  │  done  │ start a pr in rich                   │ 2024-11-12 │ 2024-11-12  │
│ 7  │  done  │ refactor template and ask            │ 2024-11-12 │ 2024-11-11  │
│ 6  │  done  │ find ICBC card                       │ 2024-11-12 │ 2024-11-12  │
│ 4  │  done  │ finish todo rm                       │ 2024-11-10 │ 2024-11-10  │
│ 3  │  done  │ go to ICBC update ID info            │ 2024-11-12 │ 2024-11-12  │
│ 1  │  done  │ add some translation                 │ 2024-11-10 │ 2024-11-10  │
└────┴────────┴──────────────────────────────────────┴────────────┴─────────────┘
```

List tasks by given status (`todo`|`done`|`expr`)

```shell
todo ls --${status}
```

More options: [`todo ls`](./docs/todo_ls.md)

### Set a Task Done

```shell
todo done ${task_id}
```

### Discard a Task

```shell
todo drop ${task_id}
```

### Remove a Task

```shell
todo rm ${task_id}
```

### Modify a Task

```shell
todo mod ${task_id}

# or use shortcut
todo m ${task_id}
```

More options: [`todo mod`](./docs/todo_mod.md)

### Edit configuration

```shell
# show configs
todo config --list

# edit configs
todo config --edit
```

- More details: [Configuration](./docs/todo_config.md)

## 4. For Developer

Install todo_cmd in editable mode

```shell
pip install -e .
```

## 5. Design

### Tech stack

- Commandline: [Rich-click](https://github.com/ewels/rich-click)
- TUI: [Rich](https://github.com/Textualize/rich)

### Documents

- [Task class](./docs/task_class.md)
  - [Task status](./docs/task_status.md)
- [Design of `todo ls`](./docs/todo_ls.md)
- [Design of `todo rm`](./docs/todo_rm.md)
- [Design of `todo mod`](./docs/todo_mod.md)
