from stringutils import word_wrap_text

with open('input.txt', mode='r', encoding='utf-8') as file:
    _input = file.read()

max_len = 80
print(f'Quebra em {max_len} colunas sem justificar:')
print('-' * max_len)
_output = word_wrap_text(_input, max_line_len=max_len, justify=False)
print(_output)
print('-' * max_len)

print('')

print(f'Quebra em {max_len} colunas justificando:')
print('-' * max_len)
_output = word_wrap_text(_input, max_line_len=max_len, justify=True)
print(_output)
print('-' * max_len)