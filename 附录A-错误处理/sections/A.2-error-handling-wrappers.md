# A.2 错误处理包装函数

下面是一些不同错误处理包装函数的示例：

- **Unix 风格的错误处理包装函数。** 图 A-2 展示了 Unix 风格的 `wait` 函数的包装函数。如果 `wait` 返回一个错误，包装函数打印一条消息，然后退出。否则，它向调用者返回一个 PID。图 A-3 展示了 Unix 风格的 `kill` 函数的包装函数。注意，这个函数和 `wait` 不同，成功时返回 `void`。

`code/src/csapp.c`

```c
pid_t Wait(int *status)
{
    pid_t pid;

    if ((pid = wait(status)) < 0)
        unix_error("Wait error");
    return pid;
}
```

**图 A-2** Unix 风格的 `wait` 函数的包装函数

`code/src/csapp.c`

```c
void Kill(pid_t pid, int signum)
{
    int rc;

    if ((rc = kill(pid, signum)) < 0)
        unix_error("Kill error");
}
```

**图 A-3** Unix 风格的 `kill` 函数的包装函数

- **Posix 风格的错误处理包装函数。** 图 A-4 展示了 Posix 风格的 `pthread_detach` 函数的包装函数。同大多数 Posix 风格的函数一样，它的错误返回码中不会包含有用的结果，所以成功时，包装函数返回 `void`。

`code/src/csapp.c`

```c
void Pthread_detach(pthread_t tid) {
    int rc;

    if ((rc = pthread_detach(tid)) != 0)
        posix_error(rc, "Pthread_detach error");
}
```

**图 A-4** Posix 风格的 `pthread_detach` 函数的包装函数

- **GAI 风格的错误处理包装函数。** 图 A-5 展示了 GAI 风格的 `getaddrinfo` 函数的包装函数。

`code/src/csapp.c`

```c
void Getaddrinfo(const char *node, const char *service,
                 const struct addrinfo *hints, struct addrinfo **res)
{
    int rc;

    if ((rc = getaddrinfo(node, service, hints, res)) != 0)
        gai_error(rc, "Getaddrinfo error");
}
```

**图 A-5** GAI 风格的 `getaddrinfo` 函数的包装函数
