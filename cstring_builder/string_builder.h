#ifndef STRING_BUILDER_H
#define STRING_BUILDER_H

#include <stddef.h>

typedef struct string_builder_s {
	char	*buff;
	size_t	buff_len;
	size_t	str_len;
}	string_builder_t;

int	strbdr_append_str(string_builder_t *strb, const char *str);
int	strbdr_append_char(string_builder_t *strb, char c);

#endif