# A.1 Unix 系统中的错误处理

本书中我们遇到的系统级函数调用使用三种不同风格的返回错误：Unix 风格的、Posix 风格的和 GAI 风格的。

## 1. Unix 风格的错误处理

像 `fork` 和 `wait` 这样 Unix 早期开发出来的函数（以及一些较老的 Posix 函数）的函数返回值既包括错误代码，也包括有用的结果。例如，当 Unix 风格的 `wait` 函数遇到一个错误（例如没有子进程要回收），它就返回 -1，并将全局变量 `errno` 设置为指明错误原因的错误代码。如果 `wait` 成功完成，那么它就返回有用的结果，也就是回收的子进程的 PID。Unix 风格的错误处理代码通常具有以下形式：

```c
if ((pid = wait(NULL)) < 0) {
    fprintf(stderr, "wait error: %s\n", strerror(errno));
    exit(0);
}
```

`strerror` 函数返回某个 `errno` 值的文本描述。

## 2. Posix 风格的错误处理

许多较新的 Posix 函数，例如 Pthread 函数，只用返回值来表明成功（0）或者失败（非 0）。任何有用的结果都返回在通过引用传递进来的函数参数中。我们称这种方法为 Posix 风格的错误处理。例如，Posix 风格的 `pthread_create` 函数用它的返回值来表明成功或者失败，而通过引用将新创建的线程的 ID（有用的结果）返回放在它的第一个参数中。Posix 风格的错误处理代码通常具有以下形式：

```c
if ((retcode = pthread_create(&tid, NULL, thread, NULL)) != 0) {
    fprintf(stderr, "pthread_create error: %s\n", strerror(retcode));
    exit(0);
}
```

`strerror` 函数返回 `retcode` 某个值对应的文本描述。

## 3. GAI 风格的错误处理

`getaddrinfo`（GAI）和 `getnameinfo` 函数成功时返回零，失败时返回非零值。GAI 错误处理代码通常具有以下形式：

```c
if ((retcode = getaddrinfo(host, service, &hints, &result)) != 0) {
    fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(retcode));
    exit(0);
}
```

`gai_strerror` 函数返回 `retcode` 某个值对应的文本描述。

## 4. 错误报告函数小结

贯穿本书，我们使用下列错误报告函数来包容不同的错误处理风格：

```c
#include "csapp.h"

void unix_error(char *msg);
void posix_error(int code, char *msg);
void gai_error(int code, char *msg);
void app_error(char *msg);
```

返回：无。

正如它们的名字表明的那样，`unix_error`、`posix_error` 和 `gai_error` 函数报告 Unix 风格的错误、Posix 风格的错误和 GAI 风格的错误，然后终止。包括 `app_error` 函数是为了方便报告应用错误。它只是简单地打印它的输入，然后终止。图 A-1 展示了这些错误报告函数的代码。

`code/src/csapp.c`

```c
void unix_error(char *msg) /* Unix-style error */
{
    fprintf(stderr, "%s: %s\n", msg, strerror(errno));
    exit(0);
}

void posix_error(int code, char *msg) /* Posix-style error */
{
    fprintf(stderr, "%s: %s\n", msg, strerror(code));
    exit(0);
}

void gai_error(int code, char *msg) /* Getaddrinfo-style error */
{
    fprintf(stderr, "%s: %s\n", msg, gai_strerror(code));
    exit(0);
}

void app_error(char *msg) /* Application error */
{
    fprintf(stderr, "%s\n", msg);
    exit(0);
}
```

**图 A-1** 错误报告函数
