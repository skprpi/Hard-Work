# full original: https://github.com/Medium/spaCy/blob/master/spacy/matcher/phrasematcher.pyx
# Overview:
#  - в коде не осталось else
#  - логические модули вынесены в отдельные функции
#  - избавление от тройной вложенности условий и циклов через вынесение логики в функции


# Cyclomatic Complexity: 10
def get_keyword(self, doc): # избавились от else + унесли логику в функцию
    if isinstance(doc, Doc):
        return doc
    if self.attr in (POS, TAG, LEMMA) and not doc.is_tagged:
        raise ValueError(Errors.E155.format())
    if self.attr == DEP and not doc.is_parsed:
        raise ValueError(Errors.E156.format())
    if self._validate and (doc.is_tagged or doc.is_parsed) \
        and self.attr not in (DEP, POS, TAG, LEMMA):
        string_attr = self.vocab.strings[self.attr]
        user_warning(Warnings.W012.format(key=key, attr=string_attr))
    keyword = self._convert_to_array(doc)
    return keyword


# Cyclomatic Complexity: 4
def fill_map_by_keyword(self, keyword):
    cdef MapStruct* current_node = self.c_map
    cdef MapStruct* internal_node
    cdef void* result

    for token in keyword:
        if token == self._terminal_hash:
            user_warning(Warnings.W021)
            return
        result = <MapStruct*>map_get(current_node, token)
        if not result:
            internal_node = <MapStruct*>self.mem.alloc(1, sizeof(MapStruct))
            map_init(self.mem, internal_node, 8)
            map_set(self.mem, current_node, token, internal_node)
            result = internal_node
        current_node = <MapStruct*>result
    return current_node, internal_node, result

# Cyclomatic Complexity: 19
# Cyclomatic Complexity now: 6
def add(self, key, docs, *_docs, on_match=None):
    if docs is None or hasattr(docs, "__call__"):  # old API
        on_match = docs
        docs = _docs

    _ = self.vocab[key]
    self._callbacks[key] = on_match
    self._docs.setdefault(key, set())

    cdef MapStruct* current_node
    cdef MapStruct* internal_node
    cdef void* result

    if isinstance(docs, Doc):
        raise ValueError(Errors.E179.format(key=key))
    for doc in docs:
        # if len(doc) == 0: continue - данная проверка не имеет смысла т к не зайдем в цикл
        keyword = self.get_keyword(doc) # унесли в функцию логику выбора keyword 
        self._docs[key].add(tuple(keyword))

        current_node, internal_node, result = self.fill_map_by_keyword(keyword) # вложенный цикл уносим в функцию
        result = <MapStruct*>map_get(current_node, self._terminal_hash)
        if not result:
            internal_node = <MapStruct*>self.mem.alloc(1, sizeof(MapStruct))
            map_init(self.mem, internal_node, 8)
            map_set(self.mem, current_node, self._terminal_hash, internal_node)
            result = internal_node
        map_set(self.mem, <MapStruct*>result, self.vocab.strings[key], NULL)
