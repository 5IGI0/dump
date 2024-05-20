#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "string_builder.h"

#define STRBLDR_S 100

static
int	strbdr_realloc_str(string_builder_t *strb, size_t needed)
{
	char	*tmp;

	if (strb->buff_len >= needed + 1)
		return (0);
	tmp = malloc((needed + 1) + STRBLDR_S - ((needed + 1) % STRBLDR_S));
	if (!tmp)
		return (-1);
	if (strb->buff)
		memcpy(tmp, strb->buff, strb->str_len + 1);
	else
		tmp[0] = '\0';
	free(strb->buff);
	strb->buff = tmp;
	return (0);
}

int	strbdr_append_str(string_builder_t *strb, const char *str)
{
	size_t	s;
	
	s = strlen(str);
	if (strbdr_realloc_str(strb, strb->str_len + s) < 0)
		return (-1);
	memcpy(strb->buff + strb->str_len, str, s + 1);
	strb->str_len += s;
	return (0);
}

int	strbdr_append_char(string_builder_t *strb, char c)
{
	if (strbdr_realloc_str(strb, strb->str_len + 1) < 0)
		return (-1);
	strb->buff[strb->str_len] = c;
	strb->buff[strb->str_len + 1] = 0;
	strb->str_len += 1;
	return (0);
}