# rev

## warmup

```c
// PSEUDOCODE -> IDA DECOMPILER

int __fastcall main(int argc, const char **argv, const char **envp)
{
  char v4[56]; // [rsp+0h] [rbp-40h] BYREF
  unsigned __int64 v5; // [rsp+38h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  printf("Enter the password: ");
  __isoc99_scanf("%49s", v4);
  if ( validate_password(v4) )
    puts("Access granted!");
  else
    puts("Access denied!");
  return 0;
}

_BOOL8 __fastcall validate_password(const char *a1)
{
  char s2[8]; // [rsp+17h] [rbp-49h] BYREF
  char v3; // [rsp+1Fh] [rbp-41h]
  char dest[56]; // [rsp+20h] [rbp-40h] BYREF
  unsigned __int64 v5; // [rsp+58h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  *(_QWORD *)s2 = 'b_I\x1ESS G';
  v3 = 0;
  strcpy(dest, a1);
  generate_key(dest);
  return strcmp(dest, s2) == 0;
}

// keygen
size_t __fastcall generate_key(const char *input)
{
  size_t result; // rax
  int i; // [rsp+1Ch] [rbp-14h]

  for ( i = 0; ; ++i )
  {
    result = strlen(input);
    if ( i >= result )
      break;
    input[i] = (input[i] ^ 0x2A) + 5;
  }
  return result;
}
```

solution

```py
solution = bytes.fromhex("625F491E53532047")[::-1]  # [::-1] wegen LE

key = str()
for i in range(len(solution)):
    for j in range(128):
        if solution[i] == (j ^ 0x2A) + 5:
            key += chr(j)
print(f"key: {key}")
```

`echo 'h1dd3npw' | ltrace ./warmup`
