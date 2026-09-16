# 练习题答案

## 练习题 11.1

| 十六进制地址 | 点分十进制地址 |
| --- | --- |
| `0x0` | `0.0.0.0` |
| `0xffffffff` | `255.255.255.255` |
| `0x7f000001` | `127.0.0.1` |
| `0xcdbca079` | `205.188.160.121` |
| `0x400c950d` | `64.12.149.13` |
| `0xcdbc9217` | `205.188.146.23` |

## 练习题 11.2

*code/netp/hex2dd.c*

```c
#include "csapp.h"

int main(int argc, char **argv)
{
    struct in_addr inaddr; /* Address in network byte order */
    uint32_t addr;         /* Address in host byte order */
    char buf[MAXBUF];     /* Buffer for dotted-decimal string */

    if (argc != 2) {
        fprintf(stderr, "usage: %s <hex number>\n", argv[0]);
        exit(0);
    }
    sscanf(argv[1], "%x", &addr);
    inaddr.s_addr = htonl(addr);

    if (!inet_ntop(AF_INET, &inaddr, buf, MAXBUF))
        unix_error("inet_ntop");
    printf("%s\n", buf);

    exit(0);
}
```

## 练习题 11.3

*code/netp/dd2hex.c*

```c
#include "csapp.h"

int main(int argc, char **argv)
{
    struct in_addr inaddr; /* Address in network byte order */
    int rc;

    if (argc != 2) {
        fprintf(stderr, "usage: %s <dotted-decimal>\n", argv[0]);
        exit(0);
    }

    rc = inet_pton(AF_INET, argv[1], &inaddr);
    if (rc == 0)
        app_error("inet_pton error: invalid dotted-decimal address");
    else if (rc < 0)
        unix_error("inet_pton error");

    printf("0x%x\n", ntohl(inaddr.s_addr));
    exit(0);
}
```

## 练习题 11.4

下面是解决方案。注意，使用 `inet_ntop` 要困难多少，它要求很麻烦的强制类型转换和深层嵌套结构引用。`getnameinfo` 函数要简单许多，因为它为我们完成了这些工作。

*code/netp/hostinfo-ntop.c*

```c
#include "csapp.h"

int main(int argc, char **argv)
{
    struct addrinfo *p, *listp, hints;
    struct sockaddr_in *sockp;
    char buf[MAXLINE];
    int rc;

    if (argc != 2) {
        fprintf(stderr, "usage: %s <domain name>\n", argv[0]);
        exit(0);
    }

    /* Get a list of addrinfo records */
    memset(&hints, 0, sizeof(struct addrinfo));
    hints.ai_family = AF_INET;       /* IPv4 only */
    hints.ai_socktype = SOCK_STREAM; /* Connections only */
    if ((rc = getaddrinfo(argv[1], NULL, &hints, &listp)) != 0) {
        fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(rc));
        exit(1);
    }

    /* Walk the list and display each associated IP address */
    for (p = listp; p; p = p->ai_next) {
        sockp = (struct sockaddr_in *)p->ai_addr;
        Inet_ntop(AF_INET, &(sockp->sin_addr), buf, MAXLINE);
        printf("%s\n", buf);
    }

    /* Clean up */
    Freeaddrinfo(listp);

    exit(0);
}
```

## 练习题 11.5

标准 I/O 能在 CGI 程序里工作的原因是，在子进程中运行的 CGI 程序不需要显式地关闭它的输入输出流。当子进程终止时，内核会自动关闭所有描述符。
