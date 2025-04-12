import msvcrt


# 密码加密显示
def jiami():
    li = []
    while 1:
        ch = msvcrt.getch()
        if ch == b'\r':     # 回车
            break
        elif ch == b'\x08':     # 退格
            if li:
                li.pop()
                msvcrt.putch(b'\b')
                msvcrt.putch(b' ')
                msvcrt.putch(b'\b')
        # Esc
        elif ch == b'\x1b':
            break
        else:
            li.append(ch)
            msvcrt.putch(b'*')
    return b''.join(li).decode()