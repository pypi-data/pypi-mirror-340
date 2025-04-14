/* Generated code for Python module 'piexif$_insert'
 * created by Nuitka version 2.5.1
 *
 * This code is in part copyright 2024 Kay Hayen.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "nuitka/prelude.h"

#include "nuitka/unfreezing.h"

#include "__helpers.h"

/* The "module_piexif$_insert" is a Python object pointer of module type.
 *
 * Note: For full compatibility with CPython, every module variable access
 * needs to go through it except for cases where the module cannot possibly
 * have changed in the mean time.
 */

PyObject *module_piexif$_insert;
PyDictObject *moduledict_piexif$_insert;

/* The declarations of module constants used, if any. */
static PyObject *mod_consts[60];
#ifndef __NUITKA_NO_ASSERT__
static Py_hash_t mod_consts_hash[60];
#endif

static PyObject *module_filename_obj = NULL;

/* Indicator if this modules private constants were created yet. */
static bool constants_created = false;

/* Function to create module private constants. */
static void createModuleConstants(PyThreadState *tstate) {
    if (constants_created == false) {
        loadConstantsBlob(tstate, &mod_consts[0], UN_TRANSLATE("piexif._insert"));
        constants_created = true;

#ifndef __NUITKA_NO_ASSERT__
        for (int i = 0; i < 60; i++) {
            mod_consts_hash[i] = DEEP_HASH(tstate, mod_consts[i]);
        }
#endif
    }
}

// We want to be able to initialize the "__main__" constants in any case.
#if 0
void createMainModuleConstants(PyThreadState *tstate) {
    createModuleConstants(tstate);
}
#endif

/* Function to verify module private constants for non-corruption. */
#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_piexif$_insert(PyThreadState *tstate) {
    // The module may not have been used at all, then ignore this.
    if (constants_created == false) return;

    for (int i = 0; i < 60; i++) {
        assert(mod_consts_hash[i] == DEEP_HASH(tstate, mod_consts[i]));
        CHECK_OBJECT_DEEP(mod_consts[i]);
    }
}
#endif

// Helper to preserving module variables for Python3.11+
#if 10
#if PYTHON_VERSION >= 0x3c0
NUITKA_MAY_BE_UNUSED static uint32_t _Nuitka_PyDictKeys_GetVersionForCurrentState(PyInterpreterState *interp, PyDictKeysObject *dk)
{
    if (dk->dk_version != 0) {
        return dk->dk_version;
    }
    uint32_t result = interp->dict_state.next_keys_version++;
    dk->dk_version = result;
    return result;
}
#elif PYTHON_VERSION >= 0x3b0
static uint32_t _Nuitka_next_dict_keys_version = 2;

NUITKA_MAY_BE_UNUSED static uint32_t _Nuitka_PyDictKeys_GetVersionForCurrentState(PyDictKeysObject *dk)
{
    if (dk->dk_version != 0) {
        return dk->dk_version;
    }
    uint32_t result = _Nuitka_next_dict_keys_version++;
    dk->dk_version = result;
    return result;
}
#endif
#endif

// Accessors to module variables.
static PyObject *module_var_accessor_piexif$_insert_$$_InvalidImageDataError(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_piexif$_insert->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_piexif$_insert->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[19]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_piexif$_insert->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[19])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[19], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[19])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[19], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[19]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[19]);
    }

    return result;
}

static PyObject *module_var_accessor_piexif$_insert_$$_ValueError(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_piexif$_insert->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_piexif$_insert->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[2]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_piexif$_insert->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[2])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[2], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[2])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[2], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[2]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[2]);
    }

    return result;
}

static PyObject *module_var_accessor_piexif$_insert_$$___spec__(PyThreadState *tstate) {
#if 0
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_piexif$_insert->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_piexif$_insert->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[59]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_piexif$_insert->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[59])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[59], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[59])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[59], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[59]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[59]);
    }

    return result;
}

static PyObject *module_var_accessor_piexif$_insert_$$__webp(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_piexif$_insert->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_piexif$_insert->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[29]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_piexif$_insert->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[29])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[29], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[29])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[29], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[29]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[29]);
    }

    return result;
}

static PyObject *module_var_accessor_piexif$_insert_$$_isinstance(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_piexif$_insert->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_piexif$_insert->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[31]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_piexif$_insert->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[31])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[31], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[31])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[31], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[31]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[31]);
    }

    return result;
}

static PyObject *module_var_accessor_piexif$_insert_$$_len(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_piexif$_insert->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_piexif$_insert->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[24]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_piexif$_insert->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[24])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[24], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[24])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[24], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[24]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[24]);
    }

    return result;
}

static PyObject *module_var_accessor_piexif$_insert_$$_merge_segments(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_piexif$_insert->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_piexif$_insert->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[27]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_piexif$_insert->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[27])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[27], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[27])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[27], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[27]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[27]);
    }

    return result;
}

static PyObject *module_var_accessor_piexif$_insert_$$_open(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_piexif$_insert->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_piexif$_insert->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[12]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_piexif$_insert->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[12])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[12], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[12])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[12], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[12]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[12]);
    }

    return result;
}

static PyObject *module_var_accessor_piexif$_insert_$$_split_into_segments(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_piexif$_insert->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_piexif$_insert->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[26]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_piexif$_insert->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[26])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[26], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[26])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[26], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[26]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[26]);
    }

    return result;
}

static PyObject *module_var_accessor_piexif$_insert_$$_struct(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_piexif$_insert->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_piexif$_insert->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[21]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_piexif$_insert->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[21])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[21], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[21])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[21], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[21]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[21]);
    }

    return result;
}


// The module code objects.
static PyCodeObject *code_objects_43258ceec97c7d5be3d32fc0d5435667;
static PyCodeObject *code_objects_252cf652602d22d3dc3693af93bc3aa7;

static void createModuleCodeObjects(void) {
    module_filename_obj = MAKE_RELATIVE_PATH(mod_consts[55]); CHECK_OBJECT(module_filename_obj);
    code_objects_43258ceec97c7d5be3d32fc0d5435667 = MAKE_CODE_OBJECT(module_filename_obj, 1, CO_NOFREE, mod_consts[56], mod_consts[56], NULL, NULL, 0, 0, 0);
    code_objects_252cf652602d22d3dc3693af93bc3aa7 = MAKE_CODE_OBJECT(module_filename_obj, 9, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE, mod_consts[30], mod_consts[30], mod_consts[57], NULL, 3, 0, 0);
}

// The module function declarations.
static PyObject *MAKE_FUNCTION_piexif$_insert$$$function__1_insert(PyObject *defaults);


// The module function definitions.
static PyObject *impl_piexif$_insert$$$function__1_insert(PyThreadState *tstate, struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = HAS_ERROR_OCCURRED(tstate);
#endif

    // Local variable declarations.
    PyObject *par_exif = python_pars[0];
    PyObject *par_image = python_pars[1];
    PyObject *par_new_file = python_pars[2];
    nuitka_bool var_output_file = NUITKA_BOOL_UNASSIGNED;
    PyObject *var_image_data = NULL;
    PyObject *var_file_type = NULL;
    PyObject *var_f = NULL;
    PyObject *var_segments = NULL;
    PyObject *var_new_data = NULL;
    PyObject *tmp_with_1__enter = NULL;
    PyObject *tmp_with_1__exit = NULL;
    nuitka_bool tmp_with_1__indicator = NUITKA_BOOL_UNASSIGNED;
    PyObject *tmp_with_1__source = NULL;
    PyObject *tmp_with_2__enter = NULL;
    PyObject *tmp_with_2__exit = NULL;
    nuitka_bool tmp_with_2__indicator = NUITKA_BOOL_UNASSIGNED;
    PyObject *tmp_with_2__source = NULL;
    PyObject *tmp_with_3__enter = NULL;
    PyObject *tmp_with_3__exit = NULL;
    nuitka_bool tmp_with_3__indicator = NUITKA_BOOL_UNASSIGNED;
    PyObject *tmp_with_3__source = NULL;
    struct Nuitka_FrameObject *frame_252cf652602d22d3dc3693af93bc3aa7;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    struct Nuitka_ExceptionPreservationItem exception_state = Empty_Nuitka_ExceptionPreservationItem;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    struct Nuitka_ExceptionStackItem exception_preserved_1;
    int tmp_res;
    bool tmp_result;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_2;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_2;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_3;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_3;
    NUITKA_MAY_BE_UNUSED nuitka_void tmp_unused;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_4;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_4;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_5;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_5;
    struct Nuitka_ExceptionStackItem exception_preserved_2;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_6;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_6;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_7;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_7;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_8;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_8;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_9;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_9;
    struct Nuitka_ExceptionStackItem exception_preserved_3;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_10;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_10;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_11;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_11;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_12;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_12;
    static struct Nuitka_FrameObject *cache_frame_252cf652602d22d3dc3693af93bc3aa7 = NULL;
    PyObject *tmp_return_value = NULL;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_13;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_13;

    // Actual function body.
    // Tried code:
    if (isFrameUnusable(cache_frame_252cf652602d22d3dc3693af93bc3aa7)) {
        Py_XDECREF(cache_frame_252cf652602d22d3dc3693af93bc3aa7);

#if _DEBUG_REFCOUNTS
        if (cache_frame_252cf652602d22d3dc3693af93bc3aa7 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_252cf652602d22d3dc3693af93bc3aa7 = MAKE_FUNCTION_FRAME(tstate, code_objects_252cf652602d22d3dc3693af93bc3aa7, module_piexif$_insert, sizeof(void *)+sizeof(nuitka_bool)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_252cf652602d22d3dc3693af93bc3aa7->m_type_description == NULL);
    frame_252cf652602d22d3dc3693af93bc3aa7 = cache_frame_252cf652602d22d3dc3693af93bc3aa7;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(tstate, frame_252cf652602d22d3dc3693af93bc3aa7);
    assert(Py_REFCNT(frame_252cf652602d22d3dc3693af93bc3aa7) == 2);

    // Framed code:
    {
        nuitka_bool tmp_condition_result_1;
        PyObject *tmp_cmp_expr_left_1;
        PyObject *tmp_cmp_expr_right_1;
        PyObject *tmp_expression_value_1;
        PyObject *tmp_subscript_value_1;
        CHECK_OBJECT(par_exif);
        tmp_expression_value_1 = par_exif;
        tmp_subscript_value_1 = mod_consts[0];
        tmp_cmp_expr_left_1 = LOOKUP_SUBSCRIPT(tstate, tmp_expression_value_1, tmp_subscript_value_1);
        if (tmp_cmp_expr_left_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_cmp_expr_right_1 = mod_consts[1];
        tmp_condition_result_1 = RICH_COMPARE_NE_NBOOL_OBJECT_BYTES(tmp_cmp_expr_left_1, tmp_cmp_expr_right_1);
        Py_DECREF(tmp_cmp_expr_left_1);
        if (tmp_condition_result_1 == NUITKA_BOOL_EXCEPTION) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        if (tmp_condition_result_1 == NUITKA_BOOL_TRUE) {
            goto branch_yes_1;
        } else {
            goto branch_no_1;
        }
    }
    branch_yes_1:;
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_called_value_1;
        tmp_called_value_1 = module_var_accessor_piexif$_insert_$$_ValueError(tstate);
        if (unlikely(tmp_called_value_1 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[2]);
        }

        if (tmp_called_value_1 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 19;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 19;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_POS_ARGS1(tstate, tmp_called_value_1, mod_consts[3]);

        if (tmp_raise_type_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 19;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        exception_state.exception_type = tmp_raise_type_1;
        exception_lineno = 19;
        RAISE_EXCEPTION_WITH_TYPE(tstate, &exception_state);
        type_description_1 = "ooobNooooo";
        goto frame_exception_exit_1;
    }
    branch_no_1:;
    {
        nuitka_bool tmp_assign_source_1;
        tmp_assign_source_1 = NUITKA_BOOL_FALSE;
        var_output_file = tmp_assign_source_1;
    }
    {
        nuitka_bool tmp_condition_result_2;
        PyObject *tmp_cmp_expr_left_2;
        PyObject *tmp_cmp_expr_right_2;
        PyObject *tmp_expression_value_2;
        PyObject *tmp_subscript_value_2;
        CHECK_OBJECT(par_image);
        tmp_expression_value_2 = par_image;
        tmp_subscript_value_2 = mod_consts[4];
        tmp_cmp_expr_left_2 = LOOKUP_SUBSCRIPT(tstate, tmp_expression_value_2, tmp_subscript_value_2);
        if (tmp_cmp_expr_left_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 25;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_cmp_expr_right_2 = mod_consts[5];
        tmp_condition_result_2 = RICH_COMPARE_EQ_NBOOL_OBJECT_BYTES(tmp_cmp_expr_left_2, tmp_cmp_expr_right_2);
        Py_DECREF(tmp_cmp_expr_left_2);
        if (tmp_condition_result_2 == NUITKA_BOOL_EXCEPTION) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 25;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        if (tmp_condition_result_2 == NUITKA_BOOL_TRUE) {
            goto branch_yes_2;
        } else {
            goto branch_no_2;
        }
    }
    branch_yes_2:;
    {
        PyObject *tmp_assign_source_2;
        CHECK_OBJECT(par_image);
        tmp_assign_source_2 = par_image;
        assert(var_image_data == NULL);
        Py_INCREF(tmp_assign_source_2);
        var_image_data = tmp_assign_source_2;
    }
    {
        PyObject *tmp_assign_source_3;
        tmp_assign_source_3 = mod_consts[6];
        assert(var_file_type == NULL);
        Py_INCREF(tmp_assign_source_3);
        var_file_type = tmp_assign_source_3;
    }
    goto branch_end_2;
    branch_no_2:;
    {
        nuitka_bool tmp_condition_result_3;
        int tmp_and_left_truth_1;
        nuitka_bool tmp_and_left_value_1;
        nuitka_bool tmp_and_right_value_1;
        PyObject *tmp_cmp_expr_left_3;
        PyObject *tmp_cmp_expr_right_3;
        PyObject *tmp_expression_value_3;
        PyObject *tmp_subscript_value_3;
        PyObject *tmp_cmp_expr_left_4;
        PyObject *tmp_cmp_expr_right_4;
        PyObject *tmp_expression_value_4;
        PyObject *tmp_subscript_value_4;
        CHECK_OBJECT(par_image);
        tmp_expression_value_3 = par_image;
        tmp_subscript_value_3 = mod_consts[7];
        tmp_cmp_expr_left_3 = LOOKUP_SUBSCRIPT(tstate, tmp_expression_value_3, tmp_subscript_value_3);
        if (tmp_cmp_expr_left_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 28;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_cmp_expr_right_3 = mod_consts[8];
        tmp_and_left_value_1 = RICH_COMPARE_EQ_NBOOL_OBJECT_BYTES(tmp_cmp_expr_left_3, tmp_cmp_expr_right_3);
        Py_DECREF(tmp_cmp_expr_left_3);
        if (tmp_and_left_value_1 == NUITKA_BOOL_EXCEPTION) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 28;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_and_left_truth_1 = tmp_and_left_value_1 == NUITKA_BOOL_TRUE ? 1 : 0;
        if (tmp_and_left_truth_1 == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 28;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        if (tmp_and_left_truth_1 == 1) {
            goto and_right_1;
        } else {
            goto and_left_1;
        }
        and_right_1:;
        CHECK_OBJECT(par_image);
        tmp_expression_value_4 = par_image;
        tmp_subscript_value_4 = mod_consts[9];
        tmp_cmp_expr_left_4 = LOOKUP_SUBSCRIPT(tstate, tmp_expression_value_4, tmp_subscript_value_4);
        if (tmp_cmp_expr_left_4 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 28;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_cmp_expr_right_4 = mod_consts[10];
        tmp_and_right_value_1 = RICH_COMPARE_EQ_NBOOL_OBJECT_BYTES(tmp_cmp_expr_left_4, tmp_cmp_expr_right_4);
        Py_DECREF(tmp_cmp_expr_left_4);
        if (tmp_and_right_value_1 == NUITKA_BOOL_EXCEPTION) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 28;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_condition_result_3 = tmp_and_right_value_1;
        goto and_end_1;
        and_left_1:;
        tmp_condition_result_3 = tmp_and_left_value_1;
        and_end_1:;
        if (tmp_condition_result_3 == NUITKA_BOOL_TRUE) {
            goto branch_yes_3;
        } else {
            goto branch_no_3;
        }
    }
    branch_yes_3:;
    {
        PyObject *tmp_assign_source_4;
        CHECK_OBJECT(par_image);
        tmp_assign_source_4 = par_image;
        assert(var_image_data == NULL);
        Py_INCREF(tmp_assign_source_4);
        var_image_data = tmp_assign_source_4;
    }
    {
        PyObject *tmp_assign_source_5;
        tmp_assign_source_5 = mod_consts[11];
        assert(var_file_type == NULL);
        Py_INCREF(tmp_assign_source_5);
        var_file_type = tmp_assign_source_5;
    }
    goto branch_end_3;
    branch_no_3:;
    // Tried code:
    {
        PyObject *tmp_assign_source_6;
        PyObject *tmp_called_value_2;
        PyObject *tmp_args_element_value_1;
        PyObject *tmp_args_element_value_2;
        tmp_called_value_2 = module_var_accessor_piexif$_insert_$$_open(tstate);
        if (unlikely(tmp_called_value_2 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[12]);
        }

        if (tmp_called_value_2 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 32;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_2;
        }
        CHECK_OBJECT(par_image);
        tmp_args_element_value_1 = par_image;
        tmp_args_element_value_2 = mod_consts[13];
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 32;
        {
            PyObject *call_args[] = {tmp_args_element_value_1, tmp_args_element_value_2};
            tmp_assign_source_6 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_2, call_args);
        }

        if (tmp_assign_source_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 32;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_2;
        }
        assert(tmp_with_1__source == NULL);
        tmp_with_1__source = tmp_assign_source_6;
    }
    {
        PyObject *tmp_assign_source_7;
        PyObject *tmp_called_value_3;
        PyObject *tmp_expression_value_5;
        CHECK_OBJECT(tmp_with_1__source);
        tmp_expression_value_5 = tmp_with_1__source;
        tmp_called_value_3 = LOOKUP_SPECIAL(tstate, tmp_expression_value_5, mod_consts[14]);
        if (tmp_called_value_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 32;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_2;
        }
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 32;
        tmp_assign_source_7 = CALL_FUNCTION_NO_ARGS(tstate, tmp_called_value_3);
        Py_DECREF(tmp_called_value_3);
        if (tmp_assign_source_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 32;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_2;
        }
        assert(tmp_with_1__enter == NULL);
        tmp_with_1__enter = tmp_assign_source_7;
    }
    {
        PyObject *tmp_assign_source_8;
        PyObject *tmp_expression_value_6;
        CHECK_OBJECT(tmp_with_1__source);
        tmp_expression_value_6 = tmp_with_1__source;
        tmp_assign_source_8 = LOOKUP_SPECIAL(tstate, tmp_expression_value_6, mod_consts[15]);
        if (tmp_assign_source_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 32;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_2;
        }
        assert(tmp_with_1__exit == NULL);
        tmp_with_1__exit = tmp_assign_source_8;
    }
    {
        nuitka_bool tmp_assign_source_9;
        tmp_assign_source_9 = NUITKA_BOOL_TRUE;
        tmp_with_1__indicator = tmp_assign_source_9;
    }
    {
        PyObject *tmp_assign_source_10;
        CHECK_OBJECT(tmp_with_1__enter);
        tmp_assign_source_10 = tmp_with_1__enter;
        assert(var_f == NULL);
        Py_INCREF(tmp_assign_source_10);
        var_f = tmp_assign_source_10;
    }
    // Tried code:
    // Tried code:
    {
        PyObject *tmp_assign_source_11;
        PyObject *tmp_called_instance_1;
        CHECK_OBJECT(var_f);
        tmp_called_instance_1 = var_f;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 33;
        tmp_assign_source_11 = CALL_METHOD_NO_ARGS(tstate, tmp_called_instance_1, mod_consts[16]);
        if (tmp_assign_source_11 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 33;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_4;
        }
        assert(var_image_data == NULL);
        var_image_data = tmp_assign_source_11;
    }
    goto try_end_1;
    // Exception handler code:
    try_except_handler_4:;
    exception_keeper_lineno_1 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_1 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    // Preserve existing published exception id 1.
    exception_preserved_1 = GET_CURRENT_EXCEPTION(tstate);

    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_keeper_name_1);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_252cf652602d22d3dc3693af93bc3aa7, exception_keeper_lineno_1);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_keeper_name_1, exception_tb);
        } else if (exception_keeper_lineno_1 != 0) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_252cf652602d22d3dc3693af93bc3aa7, exception_keeper_lineno_1);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_keeper_name_1, exception_tb);
        }
    }

    PUBLISH_CURRENT_EXCEPTION(tstate, &exception_keeper_name_1);
    // Tried code:
    {
        bool tmp_condition_result_4;
        PyObject *tmp_cmp_expr_left_5;
        PyObject *tmp_cmp_expr_right_5;
        tmp_cmp_expr_left_5 = EXC_TYPE(tstate);
        tmp_cmp_expr_right_5 = PyExc_BaseException;
        tmp_res = EXCEPTION_MATCH_BOOL(tstate, tmp_cmp_expr_left_5, tmp_cmp_expr_right_5);
        assert(!(tmp_res == -1));
        tmp_condition_result_4 = (tmp_res != 0) ? true : false;
        if (tmp_condition_result_4 != false) {
            goto branch_yes_4;
        } else {
            goto branch_no_4;
        }
    }
    branch_yes_4:;
    {
        nuitka_bool tmp_assign_source_12;
        tmp_assign_source_12 = NUITKA_BOOL_FALSE;
        tmp_with_1__indicator = tmp_assign_source_12;
    }
    {
        bool tmp_condition_result_5;
        PyObject *tmp_operand_value_1;
        PyObject *tmp_called_value_4;
        PyObject *tmp_args_element_value_3;
        PyObject *tmp_args_element_value_4;
        PyObject *tmp_args_element_value_5;
        CHECK_OBJECT(tmp_with_1__exit);
        tmp_called_value_4 = tmp_with_1__exit;
        tmp_args_element_value_3 = EXC_TYPE(tstate);
        tmp_args_element_value_4 = EXC_VALUE(tstate);
        CHECK_OBJECT(tmp_args_element_value_4); 
        tmp_args_element_value_5 = (PyObject *)EXC_TRACEBACK(tstate);
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 32;
        {
            PyObject *call_args[] = {tmp_args_element_value_3, tmp_args_element_value_4, tmp_args_element_value_5};
            tmp_operand_value_1 = CALL_FUNCTION_WITH_ARGS3(tstate, tmp_called_value_4, call_args);
        }

        if (tmp_operand_value_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 32;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_5;
        }
        tmp_res = CHECK_IF_TRUE(tmp_operand_value_1);
        Py_DECREF(tmp_operand_value_1);
        if (tmp_res == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 32;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_5;
        }
        tmp_condition_result_5 = (tmp_res == 0) ? true : false;
        if (tmp_condition_result_5 != false) {
            goto branch_yes_5;
        } else {
            goto branch_no_5;
        }
    }
    branch_yes_5:;
    tmp_result = RERAISE_EXCEPTION(tstate, &exception_state);
    if (unlikely(tmp_result == false)) {
        exception_lineno = 32;
    }

    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);

        if ((exception_tb != NULL) && (exception_tb->tb_frame == &frame_252cf652602d22d3dc3693af93bc3aa7->m_frame)) {
            frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = exception_tb->tb_lineno;
        }
    }
    type_description_1 = "ooobNooooo";
    goto try_except_handler_5;
    branch_no_5:;
    goto branch_end_4;
    branch_no_4:;
    tmp_result = RERAISE_EXCEPTION(tstate, &exception_state);
    if (unlikely(tmp_result == false)) {
        exception_lineno = 32;
    }

    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);

        if ((exception_tb != NULL) && (exception_tb->tb_frame == &frame_252cf652602d22d3dc3693af93bc3aa7->m_frame)) {
            frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = exception_tb->tb_lineno;
        }
    }
    type_description_1 = "ooobNooooo";
    goto try_except_handler_5;
    branch_end_4:;
    goto try_end_2;
    // Exception handler code:
    try_except_handler_5:;
    exception_keeper_lineno_2 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_2 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    // Restore previous exception id 1.
    SET_CURRENT_EXCEPTION(tstate, &exception_preserved_1);

    // Re-raise.
    exception_state = exception_keeper_name_2;
    exception_lineno = exception_keeper_lineno_2;

    goto try_except_handler_3;
    // End of try:
    try_end_2:;
    // Restore previous exception id 1.
    SET_CURRENT_EXCEPTION(tstate, &exception_preserved_1);

    goto try_end_1;
    NUITKA_CANNOT_GET_HERE("exception handler codes exits in all cases");
    return NULL;
    // End of try:
    try_end_1:;
    goto try_end_3;
    // Exception handler code:
    try_except_handler_3:;
    exception_keeper_lineno_3 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_3 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    {
        bool tmp_condition_result_6;
        nuitka_bool tmp_cmp_expr_left_6;
        nuitka_bool tmp_cmp_expr_right_6;
        assert(tmp_with_1__indicator != NUITKA_BOOL_UNASSIGNED);
        tmp_cmp_expr_left_6 = tmp_with_1__indicator;
        tmp_cmp_expr_right_6 = NUITKA_BOOL_TRUE;
        tmp_condition_result_6 = (tmp_cmp_expr_left_6 == tmp_cmp_expr_right_6) ? true : false;
        if (tmp_condition_result_6 != false) {
            goto branch_yes_6;
        } else {
            goto branch_no_6;
        }
    }
    branch_yes_6:;
    {
        PyObject *tmp_called_value_5;
        PyObject *tmp_call_result_1;
        CHECK_OBJECT(tmp_with_1__exit);
        tmp_called_value_5 = tmp_with_1__exit;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 32;
        tmp_call_result_1 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_5, mod_consts[17]);

        if (tmp_call_result_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);

            RELEASE_ERROR_OCCURRED_STATE(&exception_keeper_name_3);

            exception_lineno = 32;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_2;
        }
        Py_DECREF(tmp_call_result_1);
    }
    branch_no_6:;
    // Re-raise.
    exception_state = exception_keeper_name_3;
    exception_lineno = exception_keeper_lineno_3;

    goto try_except_handler_2;
    // End of try:
    try_end_3:;
    {
        bool tmp_condition_result_7;
        nuitka_bool tmp_cmp_expr_left_7;
        nuitka_bool tmp_cmp_expr_right_7;
        assert(tmp_with_1__indicator != NUITKA_BOOL_UNASSIGNED);
        tmp_cmp_expr_left_7 = tmp_with_1__indicator;
        tmp_cmp_expr_right_7 = NUITKA_BOOL_TRUE;
        tmp_condition_result_7 = (tmp_cmp_expr_left_7 == tmp_cmp_expr_right_7) ? true : false;
        if (tmp_condition_result_7 != false) {
            goto branch_yes_7;
        } else {
            goto branch_no_7;
        }
    }
    branch_yes_7:;
    {
        PyObject *tmp_called_value_6;
        PyObject *tmp_call_result_2;
        CHECK_OBJECT(tmp_with_1__exit);
        tmp_called_value_6 = tmp_with_1__exit;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 32;
        tmp_call_result_2 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_6, mod_consts[17]);

        if (tmp_call_result_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 32;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_2;
        }
        Py_DECREF(tmp_call_result_2);
    }
    branch_no_7:;
    goto try_end_4;
    // Exception handler code:
    try_except_handler_2:;
    exception_keeper_lineno_4 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_4 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    Py_XDECREF(tmp_with_1__source);
    tmp_with_1__source = NULL;
    Py_XDECREF(tmp_with_1__enter);
    tmp_with_1__enter = NULL;
    Py_XDECREF(tmp_with_1__exit);
    tmp_with_1__exit = NULL;
    // Re-raise.
    exception_state = exception_keeper_name_4;
    exception_lineno = exception_keeper_lineno_4;

    goto frame_exception_exit_1;
    // End of try:
    try_end_4:;
    CHECK_OBJECT(tmp_with_1__source);
    Py_DECREF(tmp_with_1__source);
    tmp_with_1__source = NULL;
    CHECK_OBJECT(tmp_with_1__enter);
    Py_DECREF(tmp_with_1__enter);
    tmp_with_1__enter = NULL;
    CHECK_OBJECT(tmp_with_1__exit);
    Py_DECREF(tmp_with_1__exit);
    tmp_with_1__exit = NULL;
    {
        nuitka_bool tmp_condition_result_8;
        PyObject *tmp_cmp_expr_left_8;
        PyObject *tmp_cmp_expr_right_8;
        PyObject *tmp_expression_value_7;
        PyObject *tmp_subscript_value_5;
        if (var_image_data == NULL) {

            FORMAT_UNBOUND_LOCAL_ERROR(tstate, &exception_state, mod_consts[18]);
            NORMALIZE_EXCEPTION_STATE(tstate, &exception_state);
            CHAIN_EXCEPTION(tstate, exception_state.exception_value);

            exception_lineno = 34;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }

        tmp_expression_value_7 = var_image_data;
        tmp_subscript_value_5 = mod_consts[4];
        tmp_cmp_expr_left_8 = LOOKUP_SUBSCRIPT(tstate, tmp_expression_value_7, tmp_subscript_value_5);
        if (tmp_cmp_expr_left_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 34;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_cmp_expr_right_8 = mod_consts[5];
        tmp_condition_result_8 = RICH_COMPARE_EQ_NBOOL_OBJECT_BYTES(tmp_cmp_expr_left_8, tmp_cmp_expr_right_8);
        Py_DECREF(tmp_cmp_expr_left_8);
        if (tmp_condition_result_8 == NUITKA_BOOL_EXCEPTION) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 34;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        if (tmp_condition_result_8 == NUITKA_BOOL_TRUE) {
            goto branch_yes_8;
        } else {
            goto branch_no_8;
        }
    }
    branch_yes_8:;
    {
        PyObject *tmp_assign_source_13;
        tmp_assign_source_13 = mod_consts[6];
        assert(var_file_type == NULL);
        Py_INCREF(tmp_assign_source_13);
        var_file_type = tmp_assign_source_13;
    }
    goto branch_end_8;
    branch_no_8:;
    {
        nuitka_bool tmp_condition_result_9;
        int tmp_and_left_truth_2;
        nuitka_bool tmp_and_left_value_2;
        nuitka_bool tmp_and_right_value_2;
        PyObject *tmp_cmp_expr_left_9;
        PyObject *tmp_cmp_expr_right_9;
        PyObject *tmp_expression_value_8;
        PyObject *tmp_subscript_value_6;
        PyObject *tmp_cmp_expr_left_10;
        PyObject *tmp_cmp_expr_right_10;
        PyObject *tmp_expression_value_9;
        PyObject *tmp_subscript_value_7;
        if (var_image_data == NULL) {

            FORMAT_UNBOUND_LOCAL_ERROR(tstate, &exception_state, mod_consts[18]);
            NORMALIZE_EXCEPTION_STATE(tstate, &exception_state);
            CHAIN_EXCEPTION(tstate, exception_state.exception_value);

            exception_lineno = 36;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }

        tmp_expression_value_8 = var_image_data;
        tmp_subscript_value_6 = mod_consts[7];
        tmp_cmp_expr_left_9 = LOOKUP_SUBSCRIPT(tstate, tmp_expression_value_8, tmp_subscript_value_6);
        if (tmp_cmp_expr_left_9 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 36;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_cmp_expr_right_9 = mod_consts[8];
        tmp_and_left_value_2 = RICH_COMPARE_EQ_NBOOL_OBJECT_BYTES(tmp_cmp_expr_left_9, tmp_cmp_expr_right_9);
        Py_DECREF(tmp_cmp_expr_left_9);
        if (tmp_and_left_value_2 == NUITKA_BOOL_EXCEPTION) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 36;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_and_left_truth_2 = tmp_and_left_value_2 == NUITKA_BOOL_TRUE ? 1 : 0;
        if (tmp_and_left_truth_2 == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 36;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        if (tmp_and_left_truth_2 == 1) {
            goto and_right_2;
        } else {
            goto and_left_2;
        }
        and_right_2:;
        if (var_image_data == NULL) {

            FORMAT_UNBOUND_LOCAL_ERROR(tstate, &exception_state, mod_consts[18]);
            NORMALIZE_EXCEPTION_STATE(tstate, &exception_state);
            CHAIN_EXCEPTION(tstate, exception_state.exception_value);

            exception_lineno = 36;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }

        tmp_expression_value_9 = var_image_data;
        tmp_subscript_value_7 = mod_consts[9];
        tmp_cmp_expr_left_10 = LOOKUP_SUBSCRIPT(tstate, tmp_expression_value_9, tmp_subscript_value_7);
        if (tmp_cmp_expr_left_10 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 36;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_cmp_expr_right_10 = mod_consts[10];
        tmp_and_right_value_2 = RICH_COMPARE_EQ_NBOOL_OBJECT_BYTES(tmp_cmp_expr_left_10, tmp_cmp_expr_right_10);
        Py_DECREF(tmp_cmp_expr_left_10);
        if (tmp_and_right_value_2 == NUITKA_BOOL_EXCEPTION) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 36;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_condition_result_9 = tmp_and_right_value_2;
        goto and_end_2;
        and_left_2:;
        tmp_condition_result_9 = tmp_and_left_value_2;
        and_end_2:;
        if (tmp_condition_result_9 == NUITKA_BOOL_TRUE) {
            goto branch_yes_9;
        } else {
            goto branch_no_9;
        }
    }
    branch_yes_9:;
    {
        PyObject *tmp_assign_source_14;
        tmp_assign_source_14 = mod_consts[11];
        assert(var_file_type == NULL);
        Py_INCREF(tmp_assign_source_14);
        var_file_type = tmp_assign_source_14;
    }
    goto branch_end_9;
    branch_no_9:;
    {
        PyObject *tmp_raise_type_2;
        tmp_raise_type_2 = module_var_accessor_piexif$_insert_$$_InvalidImageDataError(tstate);
        if (unlikely(tmp_raise_type_2 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[19]);
        }

        if (tmp_raise_type_2 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 39;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        exception_state.exception_type = tmp_raise_type_2;
        Py_INCREF(tmp_raise_type_2);
        exception_lineno = 39;
        RAISE_EXCEPTION_WITH_TYPE(tstate, &exception_state);
        type_description_1 = "ooobNooooo";
        goto frame_exception_exit_1;
    }
    branch_end_9:;
    branch_end_8:;
    {
        nuitka_bool tmp_assign_source_15;
        tmp_assign_source_15 = NUITKA_BOOL_TRUE;
        var_output_file = tmp_assign_source_15;
    }
    branch_end_3:;
    branch_end_2:;
    {
        bool tmp_condition_result_10;
        PyObject *tmp_cmp_expr_left_11;
        PyObject *tmp_cmp_expr_right_11;
        CHECK_OBJECT(var_file_type);
        tmp_cmp_expr_left_11 = var_file_type;
        tmp_cmp_expr_right_11 = mod_consts[6];
        tmp_condition_result_10 = RICH_COMPARE_EQ_CBOOL_UNICODE_UNICODE(tmp_cmp_expr_left_11, tmp_cmp_expr_right_11);
        if (tmp_condition_result_10 != false) {
            goto branch_yes_10;
        } else {
            goto branch_no_10;
        }
    }
    branch_yes_10:;
    {
        PyObject *tmp_assign_source_16;
        PyObject *tmp_add_expr_left_1;
        PyObject *tmp_add_expr_right_1;
        PyObject *tmp_add_expr_left_2;
        PyObject *tmp_add_expr_right_2;
        PyObject *tmp_called_value_7;
        PyObject *tmp_expression_value_10;
        PyObject *tmp_args_element_value_6;
        PyObject *tmp_args_element_value_7;
        PyObject *tmp_add_expr_left_3;
        PyObject *tmp_add_expr_right_3;
        PyObject *tmp_called_value_8;
        PyObject *tmp_args_element_value_8;
        tmp_add_expr_left_2 = mod_consts[20];
        tmp_expression_value_10 = module_var_accessor_piexif$_insert_$$_struct(tstate);
        if (unlikely(tmp_expression_value_10 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[21]);
        }

        if (tmp_expression_value_10 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 43;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_7 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_10, mod_consts[22]);
        if (tmp_called_value_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 43;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_args_element_value_6 = mod_consts[23];
        tmp_called_value_8 = module_var_accessor_piexif$_insert_$$_len(tstate);
        if (unlikely(tmp_called_value_8 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[24]);
        }

        if (tmp_called_value_8 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_7);

            exception_lineno = 43;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_exif);
        tmp_args_element_value_8 = par_exif;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 43;
        tmp_add_expr_left_3 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_8, tmp_args_element_value_8);
        if (tmp_add_expr_left_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_7);

            exception_lineno = 43;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_add_expr_right_3 = mod_consts[25];
        tmp_args_element_value_7 = BINARY_OPERATION_ADD_OBJECT_OBJECT_LONG(tmp_add_expr_left_3, tmp_add_expr_right_3);
        Py_DECREF(tmp_add_expr_left_3);
        if (tmp_args_element_value_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_7);

            exception_lineno = 43;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 43;
        {
            PyObject *call_args[] = {tmp_args_element_value_6, tmp_args_element_value_7};
            tmp_add_expr_right_2 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_7, call_args);
        }

        Py_DECREF(tmp_called_value_7);
        Py_DECREF(tmp_args_element_value_7);
        if (tmp_add_expr_right_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 43;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_add_expr_left_1 = BINARY_OPERATION_ADD_OBJECT_BYTES_OBJECT(tmp_add_expr_left_2, tmp_add_expr_right_2);
        Py_DECREF(tmp_add_expr_right_2);
        if (tmp_add_expr_left_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 43;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_exif);
        tmp_add_expr_right_1 = par_exif;
        tmp_assign_source_16 = BINARY_OPERATION_ADD_OBJECT_OBJECT_OBJECT(tmp_add_expr_left_1, tmp_add_expr_right_1);
        Py_DECREF(tmp_add_expr_left_1);
        if (tmp_assign_source_16 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 43;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        {
            PyObject *old = par_exif;
            assert(old != NULL);
            par_exif = tmp_assign_source_16;
            Py_DECREF(old);
        }

    }
    {
        PyObject *tmp_assign_source_17;
        PyObject *tmp_called_value_9;
        PyObject *tmp_args_element_value_9;
        tmp_called_value_9 = module_var_accessor_piexif$_insert_$$_split_into_segments(tstate);
        if (unlikely(tmp_called_value_9 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[26]);
        }

        if (tmp_called_value_9 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 44;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        if (var_image_data == NULL) {

            FORMAT_UNBOUND_LOCAL_ERROR(tstate, &exception_state, mod_consts[18]);
            NORMALIZE_EXCEPTION_STATE(tstate, &exception_state);
            CHAIN_EXCEPTION(tstate, exception_state.exception_value);

            exception_lineno = 44;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }

        tmp_args_element_value_9 = var_image_data;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 44;
        tmp_assign_source_17 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_9, tmp_args_element_value_9);
        if (tmp_assign_source_17 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 44;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        assert(var_segments == NULL);
        var_segments = tmp_assign_source_17;
    }
    {
        PyObject *tmp_assign_source_18;
        PyObject *tmp_called_value_10;
        PyObject *tmp_args_element_value_10;
        PyObject *tmp_args_element_value_11;
        tmp_called_value_10 = module_var_accessor_piexif$_insert_$$_merge_segments(tstate);
        if (unlikely(tmp_called_value_10 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[27]);
        }

        if (tmp_called_value_10 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 45;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(var_segments);
        tmp_args_element_value_10 = var_segments;
        CHECK_OBJECT(par_exif);
        tmp_args_element_value_11 = par_exif;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 45;
        {
            PyObject *call_args[] = {tmp_args_element_value_10, tmp_args_element_value_11};
            tmp_assign_source_18 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_10, call_args);
        }

        if (tmp_assign_source_18 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 45;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        assert(var_new_data == NULL);
        var_new_data = tmp_assign_source_18;
    }
    goto branch_end_10;
    branch_no_10:;
    {
        bool tmp_condition_result_11;
        PyObject *tmp_cmp_expr_left_12;
        PyObject *tmp_cmp_expr_right_12;
        CHECK_OBJECT(var_file_type);
        tmp_cmp_expr_left_12 = var_file_type;
        tmp_cmp_expr_right_12 = mod_consts[11];
        tmp_condition_result_11 = RICH_COMPARE_EQ_CBOOL_UNICODE_UNICODE(tmp_cmp_expr_left_12, tmp_cmp_expr_right_12);
        if (tmp_condition_result_11 != false) {
            goto branch_yes_11;
        } else {
            goto branch_no_11;
        }
    }
    branch_yes_11:;
    {
        PyObject *tmp_assign_source_19;
        PyObject *tmp_expression_value_11;
        PyObject *tmp_subscript_value_8;
        CHECK_OBJECT(par_exif);
        tmp_expression_value_11 = par_exif;
        tmp_subscript_value_8 = mod_consts[28];
        tmp_assign_source_19 = LOOKUP_SUBSCRIPT(tstate, tmp_expression_value_11, tmp_subscript_value_8);
        if (tmp_assign_source_19 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 47;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        {
            PyObject *old = par_exif;
            assert(old != NULL);
            par_exif = tmp_assign_source_19;
            Py_DECREF(old);
        }

    }
    {
        PyObject *tmp_assign_source_20;
        PyObject *tmp_called_value_11;
        PyObject *tmp_expression_value_12;
        PyObject *tmp_args_element_value_12;
        PyObject *tmp_args_element_value_13;
        tmp_expression_value_12 = module_var_accessor_piexif$_insert_$$__webp(tstate);
        if (unlikely(tmp_expression_value_12 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[29]);
        }

        if (tmp_expression_value_12 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 48;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_11 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_12, mod_consts[30]);
        if (tmp_called_value_11 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 48;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        if (var_image_data == NULL) {
            Py_DECREF(tmp_called_value_11);
            FORMAT_UNBOUND_LOCAL_ERROR(tstate, &exception_state, mod_consts[18]);
            NORMALIZE_EXCEPTION_STATE(tstate, &exception_state);
            CHAIN_EXCEPTION(tstate, exception_state.exception_value);

            exception_lineno = 48;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }

        tmp_args_element_value_12 = var_image_data;
        CHECK_OBJECT(par_exif);
        tmp_args_element_value_13 = par_exif;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 48;
        {
            PyObject *call_args[] = {tmp_args_element_value_12, tmp_args_element_value_13};
            tmp_assign_source_20 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_11, call_args);
        }

        Py_DECREF(tmp_called_value_11);
        if (tmp_assign_source_20 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 48;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        assert(var_new_data == NULL);
        var_new_data = tmp_assign_source_20;
    }
    branch_no_11:;
    branch_end_10:;
    {
        nuitka_bool tmp_condition_result_12;
        PyObject *tmp_called_value_12;
        PyObject *tmp_call_result_3;
        PyObject *tmp_args_element_value_14;
        PyObject *tmp_args_element_value_15;
        int tmp_truth_name_1;
        tmp_called_value_12 = module_var_accessor_piexif$_insert_$$_isinstance(tstate);
        if (unlikely(tmp_called_value_12 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[31]);
        }

        if (tmp_called_value_12 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 50;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_new_file);
        tmp_args_element_value_14 = par_new_file;
        {
            PyObject *hard_module = IMPORT_HARD_IO();
            tmp_args_element_value_15 = LOOKUP_ATTRIBUTE(tstate, hard_module, mod_consts[32]);
        }
        assert(!(tmp_args_element_value_15 == NULL));
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 50;
        {
            PyObject *call_args[] = {tmp_args_element_value_14, tmp_args_element_value_15};
            tmp_call_result_3 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_12, call_args);
        }

        Py_DECREF(tmp_args_element_value_15);
        if (tmp_call_result_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 50;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_truth_name_1 = CHECK_IF_TRUE(tmp_call_result_3);
        if (tmp_truth_name_1 == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_call_result_3);

            exception_lineno = 50;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_condition_result_12 = tmp_truth_name_1 == 0 ? NUITKA_BOOL_FALSE : NUITKA_BOOL_TRUE;
        Py_DECREF(tmp_call_result_3);
        if (tmp_condition_result_12 == NUITKA_BOOL_TRUE) {
            goto branch_yes_12;
        } else {
            goto branch_no_12;
        }
    }
    branch_yes_12:;
    {
        PyObject *tmp_called_value_13;
        PyObject *tmp_expression_value_13;
        PyObject *tmp_call_result_4;
        PyObject *tmp_args_element_value_16;
        CHECK_OBJECT(par_new_file);
        tmp_expression_value_13 = par_new_file;
        tmp_called_value_13 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_13, mod_consts[33]);
        if (tmp_called_value_13 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 51;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        if (var_new_data == NULL) {
            Py_DECREF(tmp_called_value_13);
            FORMAT_UNBOUND_LOCAL_ERROR(tstate, &exception_state, mod_consts[34]);
            NORMALIZE_EXCEPTION_STATE(tstate, &exception_state);
            CHAIN_EXCEPTION(tstate, exception_state.exception_value);

            exception_lineno = 51;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }

        tmp_args_element_value_16 = var_new_data;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 51;
        tmp_call_result_4 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_13, tmp_args_element_value_16);
        Py_DECREF(tmp_called_value_13);
        if (tmp_call_result_4 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 51;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_4);
    }
    {
        PyObject *tmp_called_instance_2;
        PyObject *tmp_call_result_5;
        CHECK_OBJECT(par_new_file);
        tmp_called_instance_2 = par_new_file;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 52;
        tmp_call_result_5 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_2,
            mod_consts[35],
            PyTuple_GET_ITEM(mod_consts[36], 0)
        );

        if (tmp_call_result_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 52;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_5);
    }
    goto branch_end_12;
    branch_no_12:;
    {
        nuitka_bool tmp_condition_result_13;
        int tmp_truth_name_2;
        CHECK_OBJECT(par_new_file);
        tmp_truth_name_2 = CHECK_IF_TRUE(par_new_file);
        if (tmp_truth_name_2 == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 53;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        tmp_condition_result_13 = tmp_truth_name_2 == 0 ? NUITKA_BOOL_FALSE : NUITKA_BOOL_TRUE;
        if (tmp_condition_result_13 == NUITKA_BOOL_TRUE) {
            goto branch_yes_13;
        } else {
            goto branch_no_13;
        }
    }
    branch_yes_13:;
    // Tried code:
    {
        PyObject *tmp_assign_source_21;
        PyObject *tmp_called_value_14;
        PyObject *tmp_args_element_value_17;
        PyObject *tmp_args_element_value_18;
        tmp_called_value_14 = module_var_accessor_piexif$_insert_$$_open(tstate);
        if (unlikely(tmp_called_value_14 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[12]);
        }

        if (tmp_called_value_14 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 54;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_6;
        }
        CHECK_OBJECT(par_new_file);
        tmp_args_element_value_17 = par_new_file;
        tmp_args_element_value_18 = mod_consts[37];
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 54;
        {
            PyObject *call_args[] = {tmp_args_element_value_17, tmp_args_element_value_18};
            tmp_assign_source_21 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_14, call_args);
        }

        if (tmp_assign_source_21 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 54;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_6;
        }
        assert(tmp_with_2__source == NULL);
        tmp_with_2__source = tmp_assign_source_21;
    }
    {
        PyObject *tmp_assign_source_22;
        PyObject *tmp_called_value_15;
        PyObject *tmp_expression_value_14;
        CHECK_OBJECT(tmp_with_2__source);
        tmp_expression_value_14 = tmp_with_2__source;
        tmp_called_value_15 = LOOKUP_SPECIAL(tstate, tmp_expression_value_14, mod_consts[14]);
        if (tmp_called_value_15 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 54;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_6;
        }
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 54;
        tmp_assign_source_22 = CALL_FUNCTION_NO_ARGS(tstate, tmp_called_value_15);
        Py_DECREF(tmp_called_value_15);
        if (tmp_assign_source_22 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 54;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_6;
        }
        assert(tmp_with_2__enter == NULL);
        tmp_with_2__enter = tmp_assign_source_22;
    }
    {
        PyObject *tmp_assign_source_23;
        PyObject *tmp_expression_value_15;
        CHECK_OBJECT(tmp_with_2__source);
        tmp_expression_value_15 = tmp_with_2__source;
        tmp_assign_source_23 = LOOKUP_SPECIAL(tstate, tmp_expression_value_15, mod_consts[15]);
        if (tmp_assign_source_23 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 54;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_6;
        }
        assert(tmp_with_2__exit == NULL);
        tmp_with_2__exit = tmp_assign_source_23;
    }
    {
        nuitka_bool tmp_assign_source_24;
        tmp_assign_source_24 = NUITKA_BOOL_TRUE;
        tmp_with_2__indicator = tmp_assign_source_24;
    }
    {
        PyObject *tmp_assign_source_25;
        CHECK_OBJECT(tmp_with_2__enter);
        tmp_assign_source_25 = tmp_with_2__enter;
        {
            PyObject *old = var_f;
            var_f = tmp_assign_source_25;
            Py_INCREF(var_f);
            Py_XDECREF(old);
        }

    }
    // Tried code:
    // Tried code:
    {
        PyObject *tmp_called_value_16;
        PyObject *tmp_expression_value_16;
        PyObject *tmp_call_result_6;
        PyObject *tmp_args_element_value_19;
        CHECK_OBJECT(var_f);
        tmp_expression_value_16 = var_f;
        tmp_called_value_16 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_16, mod_consts[33]);
        if (tmp_called_value_16 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 55;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_8;
        }
        if (var_new_data == NULL) {
            Py_DECREF(tmp_called_value_16);
            FORMAT_UNBOUND_LOCAL_ERROR(tstate, &exception_state, mod_consts[34]);
            NORMALIZE_EXCEPTION_STATE(tstate, &exception_state);
            CHAIN_EXCEPTION(tstate, exception_state.exception_value);

            exception_lineno = 55;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_8;
        }

        tmp_args_element_value_19 = var_new_data;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 55;
        tmp_call_result_6 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_16, tmp_args_element_value_19);
        Py_DECREF(tmp_called_value_16);
        if (tmp_call_result_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 55;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_8;
        }
        Py_DECREF(tmp_call_result_6);
    }
    goto try_end_5;
    // Exception handler code:
    try_except_handler_8:;
    exception_keeper_lineno_5 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_5 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    // Preserve existing published exception id 2.
    exception_preserved_2 = GET_CURRENT_EXCEPTION(tstate);

    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_keeper_name_5);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_252cf652602d22d3dc3693af93bc3aa7, exception_keeper_lineno_5);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_keeper_name_5, exception_tb);
        } else if (exception_keeper_lineno_5 != 0) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_252cf652602d22d3dc3693af93bc3aa7, exception_keeper_lineno_5);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_keeper_name_5, exception_tb);
        }
    }

    PUBLISH_CURRENT_EXCEPTION(tstate, &exception_keeper_name_5);
    // Tried code:
    {
        bool tmp_condition_result_14;
        PyObject *tmp_cmp_expr_left_13;
        PyObject *tmp_cmp_expr_right_13;
        tmp_cmp_expr_left_13 = EXC_TYPE(tstate);
        tmp_cmp_expr_right_13 = PyExc_BaseException;
        tmp_res = EXCEPTION_MATCH_BOOL(tstate, tmp_cmp_expr_left_13, tmp_cmp_expr_right_13);
        assert(!(tmp_res == -1));
        tmp_condition_result_14 = (tmp_res != 0) ? true : false;
        if (tmp_condition_result_14 != false) {
            goto branch_yes_14;
        } else {
            goto branch_no_14;
        }
    }
    branch_yes_14:;
    {
        nuitka_bool tmp_assign_source_26;
        tmp_assign_source_26 = NUITKA_BOOL_FALSE;
        tmp_with_2__indicator = tmp_assign_source_26;
    }
    {
        bool tmp_condition_result_15;
        PyObject *tmp_operand_value_2;
        PyObject *tmp_called_value_17;
        PyObject *tmp_args_element_value_20;
        PyObject *tmp_args_element_value_21;
        PyObject *tmp_args_element_value_22;
        CHECK_OBJECT(tmp_with_2__exit);
        tmp_called_value_17 = tmp_with_2__exit;
        tmp_args_element_value_20 = EXC_TYPE(tstate);
        tmp_args_element_value_21 = EXC_VALUE(tstate);
        CHECK_OBJECT(tmp_args_element_value_21); 
        tmp_args_element_value_22 = (PyObject *)EXC_TRACEBACK(tstate);
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 54;
        {
            PyObject *call_args[] = {tmp_args_element_value_20, tmp_args_element_value_21, tmp_args_element_value_22};
            tmp_operand_value_2 = CALL_FUNCTION_WITH_ARGS3(tstate, tmp_called_value_17, call_args);
        }

        if (tmp_operand_value_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 54;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_9;
        }
        tmp_res = CHECK_IF_TRUE(tmp_operand_value_2);
        Py_DECREF(tmp_operand_value_2);
        if (tmp_res == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 54;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_9;
        }
        tmp_condition_result_15 = (tmp_res == 0) ? true : false;
        if (tmp_condition_result_15 != false) {
            goto branch_yes_15;
        } else {
            goto branch_no_15;
        }
    }
    branch_yes_15:;
    tmp_result = RERAISE_EXCEPTION(tstate, &exception_state);
    if (unlikely(tmp_result == false)) {
        exception_lineno = 54;
    }

    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);

        if ((exception_tb != NULL) && (exception_tb->tb_frame == &frame_252cf652602d22d3dc3693af93bc3aa7->m_frame)) {
            frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = exception_tb->tb_lineno;
        }
    }
    type_description_1 = "ooobNooooo";
    goto try_except_handler_9;
    branch_no_15:;
    goto branch_end_14;
    branch_no_14:;
    tmp_result = RERAISE_EXCEPTION(tstate, &exception_state);
    if (unlikely(tmp_result == false)) {
        exception_lineno = 54;
    }

    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);

        if ((exception_tb != NULL) && (exception_tb->tb_frame == &frame_252cf652602d22d3dc3693af93bc3aa7->m_frame)) {
            frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = exception_tb->tb_lineno;
        }
    }
    type_description_1 = "ooobNooooo";
    goto try_except_handler_9;
    branch_end_14:;
    goto try_end_6;
    // Exception handler code:
    try_except_handler_9:;
    exception_keeper_lineno_6 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_6 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    // Restore previous exception id 2.
    SET_CURRENT_EXCEPTION(tstate, &exception_preserved_2);

    // Re-raise.
    exception_state = exception_keeper_name_6;
    exception_lineno = exception_keeper_lineno_6;

    goto try_except_handler_7;
    // End of try:
    try_end_6:;
    // Restore previous exception id 2.
    SET_CURRENT_EXCEPTION(tstate, &exception_preserved_2);

    goto try_end_5;
    NUITKA_CANNOT_GET_HERE("exception handler codes exits in all cases");
    return NULL;
    // End of try:
    try_end_5:;
    goto try_end_7;
    // Exception handler code:
    try_except_handler_7:;
    exception_keeper_lineno_7 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_7 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    {
        bool tmp_condition_result_16;
        nuitka_bool tmp_cmp_expr_left_14;
        nuitka_bool tmp_cmp_expr_right_14;
        assert(tmp_with_2__indicator != NUITKA_BOOL_UNASSIGNED);
        tmp_cmp_expr_left_14 = tmp_with_2__indicator;
        tmp_cmp_expr_right_14 = NUITKA_BOOL_TRUE;
        tmp_condition_result_16 = (tmp_cmp_expr_left_14 == tmp_cmp_expr_right_14) ? true : false;
        if (tmp_condition_result_16 != false) {
            goto branch_yes_16;
        } else {
            goto branch_no_16;
        }
    }
    branch_yes_16:;
    {
        PyObject *tmp_called_value_18;
        PyObject *tmp_call_result_7;
        CHECK_OBJECT(tmp_with_2__exit);
        tmp_called_value_18 = tmp_with_2__exit;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 54;
        tmp_call_result_7 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_18, mod_consts[17]);

        if (tmp_call_result_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);

            RELEASE_ERROR_OCCURRED_STATE(&exception_keeper_name_7);

            exception_lineno = 54;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_6;
        }
        Py_DECREF(tmp_call_result_7);
    }
    branch_no_16:;
    // Re-raise.
    exception_state = exception_keeper_name_7;
    exception_lineno = exception_keeper_lineno_7;

    goto try_except_handler_6;
    // End of try:
    try_end_7:;
    {
        bool tmp_condition_result_17;
        nuitka_bool tmp_cmp_expr_left_15;
        nuitka_bool tmp_cmp_expr_right_15;
        assert(tmp_with_2__indicator != NUITKA_BOOL_UNASSIGNED);
        tmp_cmp_expr_left_15 = tmp_with_2__indicator;
        tmp_cmp_expr_right_15 = NUITKA_BOOL_TRUE;
        tmp_condition_result_17 = (tmp_cmp_expr_left_15 == tmp_cmp_expr_right_15) ? true : false;
        if (tmp_condition_result_17 != false) {
            goto branch_yes_17;
        } else {
            goto branch_no_17;
        }
    }
    branch_yes_17:;
    {
        PyObject *tmp_called_value_19;
        PyObject *tmp_call_result_8;
        CHECK_OBJECT(tmp_with_2__exit);
        tmp_called_value_19 = tmp_with_2__exit;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 54;
        tmp_call_result_8 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_19, mod_consts[17]);

        if (tmp_call_result_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 54;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_6;
        }
        Py_DECREF(tmp_call_result_8);
    }
    branch_no_17:;
    goto try_end_8;
    // Exception handler code:
    try_except_handler_6:;
    exception_keeper_lineno_8 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_8 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    Py_XDECREF(tmp_with_2__source);
    tmp_with_2__source = NULL;
    Py_XDECREF(tmp_with_2__enter);
    tmp_with_2__enter = NULL;
    Py_XDECREF(tmp_with_2__exit);
    tmp_with_2__exit = NULL;
    // Re-raise.
    exception_state = exception_keeper_name_8;
    exception_lineno = exception_keeper_lineno_8;

    goto frame_exception_exit_1;
    // End of try:
    try_end_8:;
    CHECK_OBJECT(tmp_with_2__source);
    Py_DECREF(tmp_with_2__source);
    tmp_with_2__source = NULL;
    CHECK_OBJECT(tmp_with_2__enter);
    Py_DECREF(tmp_with_2__enter);
    tmp_with_2__enter = NULL;
    CHECK_OBJECT(tmp_with_2__exit);
    Py_DECREF(tmp_with_2__exit);
    tmp_with_2__exit = NULL;
    goto branch_end_13;
    branch_no_13:;
    {
        bool tmp_condition_result_18;
        assert(var_output_file != NUITKA_BOOL_UNASSIGNED);
        tmp_condition_result_18 = var_output_file == NUITKA_BOOL_TRUE;
        if (tmp_condition_result_18 != false) {
            goto branch_yes_18;
        } else {
            goto branch_no_18;
        }
    }
    branch_yes_18:;
    // Tried code:
    {
        PyObject *tmp_assign_source_27;
        PyObject *tmp_called_value_20;
        PyObject *tmp_args_element_value_23;
        PyObject *tmp_args_element_value_24;
        tmp_called_value_20 = module_var_accessor_piexif$_insert_$$_open(tstate);
        if (unlikely(tmp_called_value_20 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[12]);
        }

        if (tmp_called_value_20 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 57;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_10;
        }
        if (par_image == NULL) {

            FORMAT_UNBOUND_LOCAL_ERROR(tstate, &exception_state, mod_consts[38]);
            NORMALIZE_EXCEPTION_STATE(tstate, &exception_state);
            CHAIN_EXCEPTION(tstate, exception_state.exception_value);

            exception_lineno = 57;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_10;
        }

        tmp_args_element_value_23 = par_image;
        tmp_args_element_value_24 = mod_consts[37];
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 57;
        {
            PyObject *call_args[] = {tmp_args_element_value_23, tmp_args_element_value_24};
            tmp_assign_source_27 = CALL_FUNCTION_WITH_ARGS2(tstate, tmp_called_value_20, call_args);
        }

        if (tmp_assign_source_27 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 57;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_10;
        }
        assert(tmp_with_3__source == NULL);
        tmp_with_3__source = tmp_assign_source_27;
    }
    {
        PyObject *tmp_assign_source_28;
        PyObject *tmp_called_value_21;
        PyObject *tmp_expression_value_17;
        CHECK_OBJECT(tmp_with_3__source);
        tmp_expression_value_17 = tmp_with_3__source;
        tmp_called_value_21 = LOOKUP_SPECIAL(tstate, tmp_expression_value_17, mod_consts[14]);
        if (tmp_called_value_21 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 57;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_10;
        }
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 57;
        tmp_assign_source_28 = CALL_FUNCTION_NO_ARGS(tstate, tmp_called_value_21);
        Py_DECREF(tmp_called_value_21);
        if (tmp_assign_source_28 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 57;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_10;
        }
        assert(tmp_with_3__enter == NULL);
        tmp_with_3__enter = tmp_assign_source_28;
    }
    {
        PyObject *tmp_assign_source_29;
        PyObject *tmp_expression_value_18;
        CHECK_OBJECT(tmp_with_3__source);
        tmp_expression_value_18 = tmp_with_3__source;
        tmp_assign_source_29 = LOOKUP_SPECIAL(tstate, tmp_expression_value_18, mod_consts[15]);
        if (tmp_assign_source_29 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 57;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_10;
        }
        assert(tmp_with_3__exit == NULL);
        tmp_with_3__exit = tmp_assign_source_29;
    }
    {
        nuitka_bool tmp_assign_source_30;
        tmp_assign_source_30 = NUITKA_BOOL_TRUE;
        tmp_with_3__indicator = tmp_assign_source_30;
    }
    {
        PyObject *tmp_assign_source_31;
        CHECK_OBJECT(tmp_with_3__enter);
        tmp_assign_source_31 = tmp_with_3__enter;
        {
            PyObject *old = var_f;
            var_f = tmp_assign_source_31;
            Py_INCREF(var_f);
            Py_XDECREF(old);
        }

    }
    // Tried code:
    // Tried code:
    {
        PyObject *tmp_called_value_22;
        PyObject *tmp_expression_value_19;
        PyObject *tmp_call_result_9;
        PyObject *tmp_args_element_value_25;
        CHECK_OBJECT(var_f);
        tmp_expression_value_19 = var_f;
        tmp_called_value_22 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_19, mod_consts[33]);
        if (tmp_called_value_22 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 58;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_12;
        }
        if (var_new_data == NULL) {
            Py_DECREF(tmp_called_value_22);
            FORMAT_UNBOUND_LOCAL_ERROR(tstate, &exception_state, mod_consts[34]);
            NORMALIZE_EXCEPTION_STATE(tstate, &exception_state);
            CHAIN_EXCEPTION(tstate, exception_state.exception_value);

            exception_lineno = 58;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_12;
        }

        tmp_args_element_value_25 = var_new_data;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 58;
        tmp_call_result_9 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_22, tmp_args_element_value_25);
        Py_DECREF(tmp_called_value_22);
        if (tmp_call_result_9 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 58;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_12;
        }
        Py_DECREF(tmp_call_result_9);
    }
    goto try_end_9;
    // Exception handler code:
    try_except_handler_12:;
    exception_keeper_lineno_9 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_9 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    // Preserve existing published exception id 3.
    exception_preserved_3 = GET_CURRENT_EXCEPTION(tstate);

    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_keeper_name_9);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_252cf652602d22d3dc3693af93bc3aa7, exception_keeper_lineno_9);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_keeper_name_9, exception_tb);
        } else if (exception_keeper_lineno_9 != 0) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_252cf652602d22d3dc3693af93bc3aa7, exception_keeper_lineno_9);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_keeper_name_9, exception_tb);
        }
    }

    PUBLISH_CURRENT_EXCEPTION(tstate, &exception_keeper_name_9);
    // Tried code:
    {
        bool tmp_condition_result_19;
        PyObject *tmp_cmp_expr_left_16;
        PyObject *tmp_cmp_expr_right_16;
        tmp_cmp_expr_left_16 = EXC_TYPE(tstate);
        tmp_cmp_expr_right_16 = PyExc_BaseException;
        tmp_res = EXCEPTION_MATCH_BOOL(tstate, tmp_cmp_expr_left_16, tmp_cmp_expr_right_16);
        assert(!(tmp_res == -1));
        tmp_condition_result_19 = (tmp_res != 0) ? true : false;
        if (tmp_condition_result_19 != false) {
            goto branch_yes_19;
        } else {
            goto branch_no_19;
        }
    }
    branch_yes_19:;
    {
        nuitka_bool tmp_assign_source_32;
        tmp_assign_source_32 = NUITKA_BOOL_FALSE;
        tmp_with_3__indicator = tmp_assign_source_32;
    }
    {
        bool tmp_condition_result_20;
        PyObject *tmp_operand_value_3;
        PyObject *tmp_called_value_23;
        PyObject *tmp_args_element_value_26;
        PyObject *tmp_args_element_value_27;
        PyObject *tmp_args_element_value_28;
        CHECK_OBJECT(tmp_with_3__exit);
        tmp_called_value_23 = tmp_with_3__exit;
        tmp_args_element_value_26 = EXC_TYPE(tstate);
        tmp_args_element_value_27 = EXC_VALUE(tstate);
        CHECK_OBJECT(tmp_args_element_value_27); 
        tmp_args_element_value_28 = (PyObject *)EXC_TRACEBACK(tstate);
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 57;
        {
            PyObject *call_args[] = {tmp_args_element_value_26, tmp_args_element_value_27, tmp_args_element_value_28};
            tmp_operand_value_3 = CALL_FUNCTION_WITH_ARGS3(tstate, tmp_called_value_23, call_args);
        }

        if (tmp_operand_value_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 57;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_13;
        }
        tmp_res = CHECK_IF_TRUE(tmp_operand_value_3);
        Py_DECREF(tmp_operand_value_3);
        if (tmp_res == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 57;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_13;
        }
        tmp_condition_result_20 = (tmp_res == 0) ? true : false;
        if (tmp_condition_result_20 != false) {
            goto branch_yes_20;
        } else {
            goto branch_no_20;
        }
    }
    branch_yes_20:;
    tmp_result = RERAISE_EXCEPTION(tstate, &exception_state);
    if (unlikely(tmp_result == false)) {
        exception_lineno = 57;
    }

    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);

        if ((exception_tb != NULL) && (exception_tb->tb_frame == &frame_252cf652602d22d3dc3693af93bc3aa7->m_frame)) {
            frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = exception_tb->tb_lineno;
        }
    }
    type_description_1 = "ooobNooooo";
    goto try_except_handler_13;
    branch_no_20:;
    goto branch_end_19;
    branch_no_19:;
    tmp_result = RERAISE_EXCEPTION(tstate, &exception_state);
    if (unlikely(tmp_result == false)) {
        exception_lineno = 57;
    }

    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);

        if ((exception_tb != NULL) && (exception_tb->tb_frame == &frame_252cf652602d22d3dc3693af93bc3aa7->m_frame)) {
            frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = exception_tb->tb_lineno;
        }
    }
    type_description_1 = "ooobNooooo";
    goto try_except_handler_13;
    branch_end_19:;
    goto try_end_10;
    // Exception handler code:
    try_except_handler_13:;
    exception_keeper_lineno_10 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_10 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    // Restore previous exception id 3.
    SET_CURRENT_EXCEPTION(tstate, &exception_preserved_3);

    // Re-raise.
    exception_state = exception_keeper_name_10;
    exception_lineno = exception_keeper_lineno_10;

    goto try_except_handler_11;
    // End of try:
    try_end_10:;
    // Restore previous exception id 3.
    SET_CURRENT_EXCEPTION(tstate, &exception_preserved_3);

    goto try_end_9;
    NUITKA_CANNOT_GET_HERE("exception handler codes exits in all cases");
    return NULL;
    // End of try:
    try_end_9:;
    goto try_end_11;
    // Exception handler code:
    try_except_handler_11:;
    exception_keeper_lineno_11 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_11 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    {
        bool tmp_condition_result_21;
        nuitka_bool tmp_cmp_expr_left_17;
        nuitka_bool tmp_cmp_expr_right_17;
        assert(tmp_with_3__indicator != NUITKA_BOOL_UNASSIGNED);
        tmp_cmp_expr_left_17 = tmp_with_3__indicator;
        tmp_cmp_expr_right_17 = NUITKA_BOOL_TRUE;
        tmp_condition_result_21 = (tmp_cmp_expr_left_17 == tmp_cmp_expr_right_17) ? true : false;
        if (tmp_condition_result_21 != false) {
            goto branch_yes_21;
        } else {
            goto branch_no_21;
        }
    }
    branch_yes_21:;
    {
        PyObject *tmp_called_value_24;
        PyObject *tmp_call_result_10;
        CHECK_OBJECT(tmp_with_3__exit);
        tmp_called_value_24 = tmp_with_3__exit;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 57;
        tmp_call_result_10 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_24, mod_consts[17]);

        if (tmp_call_result_10 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);

            RELEASE_ERROR_OCCURRED_STATE(&exception_keeper_name_11);

            exception_lineno = 57;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_10;
        }
        Py_DECREF(tmp_call_result_10);
    }
    branch_no_21:;
    // Re-raise.
    exception_state = exception_keeper_name_11;
    exception_lineno = exception_keeper_lineno_11;

    goto try_except_handler_10;
    // End of try:
    try_end_11:;
    {
        bool tmp_condition_result_22;
        nuitka_bool tmp_cmp_expr_left_18;
        nuitka_bool tmp_cmp_expr_right_18;
        assert(tmp_with_3__indicator != NUITKA_BOOL_UNASSIGNED);
        tmp_cmp_expr_left_18 = tmp_with_3__indicator;
        tmp_cmp_expr_right_18 = NUITKA_BOOL_TRUE;
        tmp_condition_result_22 = (tmp_cmp_expr_left_18 == tmp_cmp_expr_right_18) ? true : false;
        if (tmp_condition_result_22 != false) {
            goto branch_yes_22;
        } else {
            goto branch_no_22;
        }
    }
    branch_yes_22:;
    {
        PyObject *tmp_called_value_25;
        PyObject *tmp_call_result_11;
        CHECK_OBJECT(tmp_with_3__exit);
        tmp_called_value_25 = tmp_with_3__exit;
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 57;
        tmp_call_result_11 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_25, mod_consts[17]);

        if (tmp_call_result_11 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 57;
            type_description_1 = "ooobNooooo";
            goto try_except_handler_10;
        }
        Py_DECREF(tmp_call_result_11);
    }
    branch_no_22:;
    goto try_end_12;
    // Exception handler code:
    try_except_handler_10:;
    exception_keeper_lineno_12 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_12 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    Py_XDECREF(tmp_with_3__source);
    tmp_with_3__source = NULL;
    Py_XDECREF(tmp_with_3__enter);
    tmp_with_3__enter = NULL;
    Py_XDECREF(tmp_with_3__exit);
    tmp_with_3__exit = NULL;
    // Re-raise.
    exception_state = exception_keeper_name_12;
    exception_lineno = exception_keeper_lineno_12;

    goto frame_exception_exit_1;
    // End of try:
    try_end_12:;
    CHECK_OBJECT(tmp_with_3__source);
    Py_DECREF(tmp_with_3__source);
    tmp_with_3__source = NULL;
    CHECK_OBJECT(tmp_with_3__enter);
    Py_DECREF(tmp_with_3__enter);
    tmp_with_3__enter = NULL;
    CHECK_OBJECT(tmp_with_3__exit);
    Py_DECREF(tmp_with_3__exit);
    tmp_with_3__exit = NULL;
    goto branch_end_18;
    branch_no_18:;
    {
        PyObject *tmp_raise_type_3;
        PyObject *tmp_called_value_26;
        tmp_called_value_26 = module_var_accessor_piexif$_insert_$$_ValueError(tstate);
        if (unlikely(tmp_called_value_26 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[2]);
        }

        if (tmp_called_value_26 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 60;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        frame_252cf652602d22d3dc3693af93bc3aa7->m_frame.f_lineno = 60;
        tmp_raise_type_3 = CALL_FUNCTION_WITH_POS_ARGS1(tstate, tmp_called_value_26, mod_consts[39]);

        if (tmp_raise_type_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 60;
            type_description_1 = "ooobNooooo";
            goto frame_exception_exit_1;
        }
        exception_state.exception_type = tmp_raise_type_3;
        exception_lineno = 60;
        RAISE_EXCEPTION_WITH_TYPE(tstate, &exception_state);
        type_description_1 = "ooobNooooo";
        goto frame_exception_exit_1;
    }
    branch_end_18:;
    branch_end_13:;
    branch_end_12:;


    // Put the previous frame back on top.
    popFrameStack(tstate);

    goto frame_no_exception_1;
    frame_exception_exit_1:


    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_252cf652602d22d3dc3693af93bc3aa7, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        } else if (exception_tb->tb_frame != &frame_252cf652602d22d3dc3693af93bc3aa7->m_frame) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_252cf652602d22d3dc3693af93bc3aa7, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        }
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_252cf652602d22d3dc3693af93bc3aa7,
        type_description_1,
        par_exif,
        par_image,
        par_new_file,
        (int)var_output_file,
        NULL,
        var_image_data,
        var_file_type,
        var_f,
        var_segments,
        var_new_data
    );


    // Release cached frame if used for exception.
    if (frame_252cf652602d22d3dc3693af93bc3aa7 == cache_frame_252cf652602d22d3dc3693af93bc3aa7) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_252cf652602d22d3dc3693af93bc3aa7);
        cache_frame_252cf652602d22d3dc3693af93bc3aa7 = NULL;
    }

    assertFrameObject(frame_252cf652602d22d3dc3693af93bc3aa7);

    // Put the previous frame back on top.
    popFrameStack(tstate);

    // Return the error.
    goto try_except_handler_1;
    frame_no_exception_1:;
    tmp_return_value = Py_None;
    Py_INCREF(tmp_return_value);
    goto try_return_handler_1;
    NUITKA_CANNOT_GET_HERE("tried codes exits in all cases");
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    Py_XDECREF(par_exif);
    par_exif = NULL;
    assert(var_output_file != NUITKA_BOOL_UNASSIGNED);
    var_output_file = NUITKA_BOOL_UNASSIGNED;
    Py_XDECREF(var_image_data);
    var_image_data = NULL;
    CHECK_OBJECT(var_file_type);
    Py_DECREF(var_file_type);
    var_file_type = NULL;
    Py_XDECREF(var_f);
    var_f = NULL;
    Py_XDECREF(var_segments);
    var_segments = NULL;
    Py_XDECREF(var_new_data);
    var_new_data = NULL;
    goto function_return_exit;
    // Exception handler code:
    try_except_handler_1:;
    exception_keeper_lineno_13 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_13 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    Py_XDECREF(par_exif);
    par_exif = NULL;
    var_output_file = NUITKA_BOOL_UNASSIGNED;
    Py_XDECREF(var_image_data);
    var_image_data = NULL;
    Py_XDECREF(var_file_type);
    var_file_type = NULL;
    Py_XDECREF(var_f);
    var_f = NULL;
    Py_XDECREF(var_segments);
    var_segments = NULL;
    Py_XDECREF(var_new_data);
    var_new_data = NULL;
    // Re-raise.
    exception_state = exception_keeper_name_13;
    exception_lineno = exception_keeper_lineno_13;

    goto function_exception_exit;
    // End of try:

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_image);
    Py_DECREF(par_image);
    CHECK_OBJECT(par_new_file);
    Py_DECREF(par_new_file);
    CHECK_EXCEPTION_STATE(&exception_state);
    RESTORE_ERROR_OCCURRED_STATE(tstate, &exception_state);

    return NULL;

function_return_exit:
   // Function cleanup code if any.
    CHECK_OBJECT(par_image);
    Py_DECREF(par_image);
    CHECK_OBJECT(par_new_file);
    Py_DECREF(par_new_file);

   // Actual function exit with return value, making sure we did not make
   // the error status worse despite non-NULL return.
   CHECK_OBJECT(tmp_return_value);
   assert(had_error || !HAS_ERROR_OCCURRED(tstate));
   return tmp_return_value;
}



static PyObject *MAKE_FUNCTION_piexif$_insert$$$function__1_insert(PyObject *defaults) {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_piexif$_insert$$$function__1_insert,
        mod_consts[30],
#if PYTHON_VERSION >= 0x300
        NULL,
#endif
        code_objects_252cf652602d22d3dc3693af93bc3aa7,
        defaults,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_piexif$_insert,
        mod_consts[40],
        NULL,
        0
    );


    return (PyObject *)result;
}


extern void _initCompiledCellType();
extern void _initCompiledGeneratorType();
extern void _initCompiledFunctionType();
extern void _initCompiledMethodType();
extern void _initCompiledFrameType();

extern PyTypeObject Nuitka_Loader_Type;

#ifdef _NUITKA_PLUGIN_DILL_ENABLED
// Provide a way to create find a function via its C code and create it back
// in another process, useful for multiprocessing extensions like dill
extern void registerDillPluginTables(PyThreadState *tstate, char const *module_name, PyMethodDef *reduce_compiled_function, PyMethodDef *create_compiled_function);

static function_impl_code const function_table_piexif$_insert[] = {
    impl_piexif$_insert$$$function__1_insert,
    NULL
};

static PyObject *_reduce_compiled_function(PyObject *self, PyObject *args, PyObject *kwds) {
    PyObject *func;

    if (!PyArg_ParseTuple(args, "O:reduce_compiled_function", &func, NULL)) {
        return NULL;
    }

    PyThreadState *tstate = PyThreadState_GET();

    if (Nuitka_Function_Check(func) == false) {
        SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_TypeError, "not a compiled function");
        return NULL;
    }

    struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)func;

    int offset = Nuitka_Function_GetFunctionCodeIndex(function, function_table_piexif$_insert);

    if (unlikely(offset == -1)) {
#if 0
        PRINT_STRING("Looking for:");
        PRINT_ITEM(func);
        PRINT_NEW_LINE();
#endif
        SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_TypeError, "Cannot find compiled function in module.");
        return NULL;
    }

    PyObject *code_object_desc = Nuitka_Function_ExtractCodeObjectDescription(tstate, function);

    PyObject *result = MAKE_TUPLE_EMPTY(tstate, 8);
    PyTuple_SET_ITEM(result, 0, Nuitka_PyLong_FromLong(offset));
    PyTuple_SET_ITEM(result, 1, code_object_desc);
    PyTuple_SET_ITEM0(result, 2, function->m_defaults);
#if PYTHON_VERSION >= 0x300
    PyTuple_SET_ITEM0(result, 3, function->m_kwdefaults ? function->m_kwdefaults : Py_None);
#else
    PyTuple_SET_ITEM_IMMORTAL(result, 3, Py_None);
#endif
    PyTuple_SET_ITEM0(result, 4, function->m_doc != NULL ? function->m_doc : Py_None);

    if (offset == -5) {
        CHECK_OBJECT(function->m_constant_return_value);
        PyTuple_SET_ITEM_IMMORTAL(result, 5, function->m_constant_return_value);
    } else {
        PyTuple_SET_ITEM_IMMORTAL(result, 5, Py_None);
    }

#if PYTHON_VERSION >= 0x300
    PyTuple_SET_ITEM0(result, 6, function->m_qualname);
#else
    PyTuple_SET_ITEM_IMMORTAL(result, 6, Py_None);
#endif

    PyObject *closure = PyObject_GetAttr(
        (PyObject *)function,
        const_str_plain___closure__
    );

    if (closure != Py_None) {
        for (Py_ssize_t i=0; i < PyTuple_GET_SIZE(closure); i++) {
            struct Nuitka_CellObject *cell = (struct Nuitka_CellObject *)PyTuple_GET_ITEM(closure, i);

            assert(Nuitka_Cell_Check((PyObject *)cell));

            PyTuple_SET_ITEM0(
                closure,
                i,
                cell->ob_ref
            );
        }
    }

    PyTuple_SET_ITEM(result, 7, closure);

    CHECK_OBJECT_DEEP(result);

    return result;
}

static PyMethodDef _method_def_reduce_compiled_function = {"reduce_compiled_function", (PyCFunction)_reduce_compiled_function,
                                                           METH_VARARGS, NULL};


static PyObject *_create_compiled_function(PyObject *self, PyObject *args, PyObject *kwds) {
    CHECK_OBJECT_DEEP(args);

    PyObject *function_index;
    PyObject *code_object_desc;
    PyObject *defaults;
    PyObject *kw_defaults;
    PyObject *doc;
    PyObject *constant_return_value;
    PyObject *function_qualname;
    PyObject *closure;

    if (!PyArg_ParseTuple(args, "OOOOOOOO:create_compiled_function", &function_index, &code_object_desc, &defaults, &kw_defaults, &doc, &constant_return_value, &function_qualname, &closure, NULL)) {
        return NULL;
    }

#if PYTHON_VERSION >= 0x300
    if (kw_defaults == Py_None) {
        kw_defaults = NULL;
    }
#endif

    return (PyObject *)Nuitka_Function_CreateFunctionViaCodeIndex(
        module_piexif$_insert,
        function_qualname,
        function_index,
        code_object_desc,
        constant_return_value,
        defaults,
        kw_defaults,
        doc,
        closure,
        function_table_piexif$_insert,
        sizeof(function_table_piexif$_insert) / sizeof(function_impl_code)
    );
}

static PyMethodDef _method_def_create_compiled_function = {
    "create_compiled_function",
    (PyCFunction)_create_compiled_function,
    METH_VARARGS, NULL
};


#endif

// Actual name might be different when loaded as a package.
#if defined(_NUITKA_MODULE) && 0
static char const *module_full_name = "piexif._insert";
#endif

// Internal entry point for module code.
PyObject *modulecode_piexif$_insert(PyThreadState *tstate, PyObject *module, struct Nuitka_MetaPathBasedLoaderEntry const *loader_entry) {
    // Report entry to PGO.
    PGO_onModuleEntered("piexif$_insert");

    // Store the module for future use.
    module_piexif$_insert = module;

    moduledict_piexif$_insert = MODULE_DICT(module_piexif$_insert);

    // Modules can be loaded again in case of errors, avoid the init being done again.
    static bool init_done = false;

    if (init_done == false) {
#if defined(_NUITKA_MODULE) && 0
        // In case of an extension module loaded into a process, we need to call
        // initialization here because that's the first and potentially only time
        // we are going called.
#if PYTHON_VERSION > 0x350 && !defined(_NUITKA_EXPERIMENTAL_DISABLE_ALLOCATORS)
        initNuitkaAllocators();
#endif
        // Initialize the constant values used.
        _initBuiltinModule();

#if PYTHON_VERSION >= 0x3c0
        PyObject *real_module_name = PyObject_GetAttrString(module, "__name__");
        CHECK_OBJECT(real_module_name);
        module_full_name = strdup(Nuitka_String_AsString(real_module_name));
#endif

#if PYTHON_VERSION >= 0x3c0
        createGlobalConstants(tstate, real_module_name);
#else
        createGlobalConstants(tstate);
#endif
        /* Initialize the compiled types of Nuitka. */
        _initCompiledCellType();
        _initCompiledGeneratorType();
        _initCompiledFunctionType();
        _initCompiledMethodType();
        _initCompiledFrameType();

        _initSlotCompare();
#if PYTHON_VERSION >= 0x270
        _initSlotIterNext();
#endif

        patchTypeComparison();

        // Enable meta path based loader if not already done.
#ifdef _NUITKA_TRACE
        PRINT_STRING("piexif$_insert: Calling setupMetaPathBasedLoader().\n");
#endif
        setupMetaPathBasedLoader(tstate);
#if PYTHON_VERSION >= 0x3c0
        updateMetaPathBasedLoaderModuleRoot(module_full_name);
#endif


#if PYTHON_VERSION >= 0x300
        patchInspectModule(tstate);
#endif

#endif

        /* The constants only used by this module are created now. */
        NUITKA_PRINT_TRACE("piexif$_insert: Calling createModuleConstants().\n");
        createModuleConstants(tstate);

        createModuleCodeObjects();

        init_done = true;
    }

#if defined(_NUITKA_MODULE) && 0
    PyObject *pre_load = IMPORT_EMBEDDED_MODULE(tstate, "piexif._insert" "-preLoad");
    if (pre_load == NULL) {
        return NULL;
    }
#endif

    // PRINT_STRING("in initpiexif$_insert\n");

#ifdef _NUITKA_PLUGIN_DILL_ENABLED
    {
        char const *module_name_c;
        if (loader_entry != NULL) {
            module_name_c = loader_entry->name;
        } else {
            PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)const_str_plain___name__);
            module_name_c = Nuitka_String_AsString(module_name);
        }

        registerDillPluginTables(tstate, module_name_c, &_method_def_reduce_compiled_function, &_method_def_create_compiled_function);
    }
#endif

    // Set "__compiled__" to what version information we have.
    UPDATE_STRING_DICT0(
        moduledict_piexif$_insert,
        (Nuitka_StringObject *)const_str_plain___compiled__,
        Nuitka_dunder_compiled_value
    );

    // Update "__package__" value to what it ought to be.
    {
#if 0
        UPDATE_STRING_DICT0(
            moduledict_piexif$_insert,
            (Nuitka_StringObject *)const_str_plain___package__,
            mod_consts[58]
        );
#elif 0
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)const_str_plain___name__);

        UPDATE_STRING_DICT0(
            moduledict_piexif$_insert,
            (Nuitka_StringObject *)const_str_plain___package__,
            module_name
        );
#else

#if PYTHON_VERSION < 0x300
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)const_str_plain___name__);
        char const *module_name_cstr = PyString_AS_STRING(module_name);

        char const *last_dot = strrchr(module_name_cstr, '.');

        if (last_dot != NULL) {
            UPDATE_STRING_DICT1(
                moduledict_piexif$_insert,
                (Nuitka_StringObject *)const_str_plain___package__,
                PyString_FromStringAndSize(module_name_cstr, last_dot - module_name_cstr)
            );
        }
#else
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)const_str_plain___name__);
        Py_ssize_t dot_index = PyUnicode_Find(module_name, const_str_dot, 0, PyUnicode_GetLength(module_name), -1);

        if (dot_index != -1) {
            UPDATE_STRING_DICT1(
                moduledict_piexif$_insert,
                (Nuitka_StringObject *)const_str_plain___package__,
                PyUnicode_Substring(module_name, 0, dot_index)
            );
        }
#endif
#endif
    }

    CHECK_OBJECT(module_piexif$_insert);

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    if (GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)const_str_plain___builtins__) == NULL) {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then but the module itself.
#if defined(_NUITKA_MODULE) || !0
        value = PyModule_GetDict(value);
#endif

        UPDATE_STRING_DICT0(moduledict_piexif$_insert, (Nuitka_StringObject *)const_str_plain___builtins__, value);
    }

    UPDATE_STRING_DICT0(moduledict_piexif$_insert, (Nuitka_StringObject *)const_str_plain___loader__, Nuitka_Loader_New(loader_entry));

#if PYTHON_VERSION >= 0x300
// Set the "__spec__" value

#if 0
    // Main modules just get "None" as spec.
    UPDATE_STRING_DICT0(moduledict_piexif$_insert, (Nuitka_StringObject *)const_str_plain___spec__, Py_None);
#else
    // Other modules get a "ModuleSpec" from the standard mechanism.
    {
        PyObject *bootstrap_module = getImportLibBootstrapModule();
        CHECK_OBJECT(bootstrap_module);

        PyObject *_spec_from_module = PyObject_GetAttrString(bootstrap_module, "_spec_from_module");
        CHECK_OBJECT(_spec_from_module);

        PyObject *spec_value = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, _spec_from_module, module_piexif$_insert);
        Py_DECREF(_spec_from_module);

        // We can assume this to never fail, or else we are in trouble anyway.
        // CHECK_OBJECT(spec_value);

        if (spec_value == NULL) {
            PyErr_PrintEx(0);
            abort();
        }

// Mark the execution in the "__spec__" value.
        SET_ATTRIBUTE(tstate, spec_value, const_str_plain__initializing, Py_True);

        UPDATE_STRING_DICT1(moduledict_piexif$_insert, (Nuitka_StringObject *)const_str_plain___spec__, spec_value);
    }
#endif
#endif

    // Temp variables if any
    struct Nuitka_FrameObject *frame_43258ceec97c7d5be3d32fc0d5435667;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    bool tmp_result;
    struct Nuitka_ExceptionPreservationItem exception_state = Empty_Nuitka_ExceptionPreservationItem;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;

    // Module init code if any


    // Module code.
    {
        PyObject *tmp_assign_source_1;
        tmp_assign_source_1 = Py_None;
        UPDATE_STRING_DICT0(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[41], tmp_assign_source_1);
    }
    {
        PyObject *tmp_assign_source_2;
        tmp_assign_source_2 = module_filename_obj;
        UPDATE_STRING_DICT0(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[42], tmp_assign_source_2);
    }
    frame_43258ceec97c7d5be3d32fc0d5435667 = MAKE_MODULE_FRAME(code_objects_43258ceec97c7d5be3d32fc0d5435667, module_piexif$_insert);

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(tstate, frame_43258ceec97c7d5be3d32fc0d5435667);
    assert(Py_REFCNT(frame_43258ceec97c7d5be3d32fc0d5435667) == 2);

    // Framed code:
    {
        PyObject *tmp_assattr_value_1;
        PyObject *tmp_assattr_target_1;
        tmp_assattr_value_1 = module_filename_obj;
        tmp_assattr_target_1 = module_var_accessor_piexif$_insert_$$___spec__(tstate);
        assert(!(tmp_assattr_target_1 == NULL));
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_1, mod_consts[43], tmp_assattr_value_1);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 1;

            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_assattr_value_2;
        PyObject *tmp_assattr_target_2;
        tmp_assattr_value_2 = Py_True;
        tmp_assattr_target_2 = module_var_accessor_piexif$_insert_$$___spec__(tstate);
        assert(!(tmp_assattr_target_2 == NULL));
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_2, mod_consts[44], tmp_assattr_value_2);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 1;

            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_assign_source_3;
        tmp_assign_source_3 = Py_None;
        UPDATE_STRING_DICT0(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[45], tmp_assign_source_3);
    }
    {
        PyObject *tmp_assign_source_4;
        tmp_assign_source_4 = IMPORT_HARD_IO();
        assert(!(tmp_assign_source_4 == NULL));
        UPDATE_STRING_DICT0(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[46], tmp_assign_source_4);
    }
    {
        PyObject *tmp_assign_source_5;
        PyObject *tmp_name_value_1;
        PyObject *tmp_globals_arg_value_1;
        PyObject *tmp_locals_arg_value_1;
        PyObject *tmp_fromlist_value_1;
        PyObject *tmp_level_value_1;
        tmp_name_value_1 = mod_consts[21];
        tmp_globals_arg_value_1 = (PyObject *)moduledict_piexif$_insert;
        tmp_locals_arg_value_1 = Py_None;
        tmp_fromlist_value_1 = Py_None;
        tmp_level_value_1 = const_int_0;
        frame_43258ceec97c7d5be3d32fc0d5435667->m_frame.f_lineno = 2;
        tmp_assign_source_5 = IMPORT_MODULE5(tstate, tmp_name_value_1, tmp_globals_arg_value_1, tmp_locals_arg_value_1, tmp_fromlist_value_1, tmp_level_value_1);
        if (tmp_assign_source_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 2;

            goto frame_exception_exit_1;
        }
        UPDATE_STRING_DICT1(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[21], tmp_assign_source_5);
    }
    {
        PyObject *tmp_assign_source_6;
        tmp_assign_source_6 = IMPORT_HARD_SYS();
        assert(!(tmp_assign_source_6 == NULL));
        UPDATE_STRING_DICT0(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[47], tmp_assign_source_6);
    }
    {
        PyObject *tmp_star_imported_1;
        PyObject *tmp_name_value_2;
        PyObject *tmp_globals_arg_value_2;
        PyObject *tmp_locals_arg_value_2;
        PyObject *tmp_fromlist_value_2;
        PyObject *tmp_level_value_2;
        tmp_name_value_2 = mod_consts[48];
        tmp_globals_arg_value_2 = (PyObject *)moduledict_piexif$_insert;
        tmp_locals_arg_value_2 = (PyObject *)moduledict_piexif$_insert;
        tmp_fromlist_value_2 = mod_consts[49];
        tmp_level_value_2 = const_int_pos_1;
        frame_43258ceec97c7d5be3d32fc0d5435667->m_frame.f_lineno = 5;
        tmp_star_imported_1 = IMPORT_MODULE5(tstate, tmp_name_value_2, tmp_globals_arg_value_2, tmp_locals_arg_value_2, tmp_fromlist_value_2, tmp_level_value_2);
        if (tmp_star_imported_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 5;

            goto frame_exception_exit_1;
        }
        tmp_result = IMPORT_MODULE_STAR(tstate, module_piexif$_insert, true, tmp_star_imported_1);
        Py_DECREF(tmp_star_imported_1);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 5;

            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_assign_source_7;
        PyObject *tmp_import_name_from_1;
        PyObject *tmp_name_value_3;
        PyObject *tmp_globals_arg_value_3;
        PyObject *tmp_locals_arg_value_3;
        PyObject *tmp_fromlist_value_3;
        PyObject *tmp_level_value_3;
        tmp_name_value_3 = mod_consts[50];
        tmp_globals_arg_value_3 = (PyObject *)moduledict_piexif$_insert;
        tmp_locals_arg_value_3 = Py_None;
        tmp_fromlist_value_3 = mod_consts[51];
        tmp_level_value_3 = const_int_pos_1;
        frame_43258ceec97c7d5be3d32fc0d5435667->m_frame.f_lineno = 6;
        tmp_import_name_from_1 = IMPORT_MODULE5(tstate, tmp_name_value_3, tmp_globals_arg_value_3, tmp_locals_arg_value_3, tmp_fromlist_value_3, tmp_level_value_3);
        if (tmp_import_name_from_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 6;

            goto frame_exception_exit_1;
        }
        if (PyModule_Check(tmp_import_name_from_1)) {
            tmp_assign_source_7 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_1,
                (PyObject *)moduledict_piexif$_insert,
                mod_consts[19],
                const_int_0
            );
        } else {
            tmp_assign_source_7 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_1, mod_consts[19]);
        }

        Py_DECREF(tmp_import_name_from_1);
        if (tmp_assign_source_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 6;

            goto frame_exception_exit_1;
        }
        UPDATE_STRING_DICT1(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[19], tmp_assign_source_7);
    }
    {
        PyObject *tmp_assign_source_8;
        PyObject *tmp_import_name_from_2;
        PyObject *tmp_name_value_4;
        PyObject *tmp_globals_arg_value_4;
        PyObject *tmp_locals_arg_value_4;
        PyObject *tmp_fromlist_value_4;
        PyObject *tmp_level_value_4;
        tmp_name_value_4 = mod_consts[52];
        tmp_globals_arg_value_4 = (PyObject *)moduledict_piexif$_insert;
        tmp_locals_arg_value_4 = Py_None;
        tmp_fromlist_value_4 = mod_consts[53];
        tmp_level_value_4 = const_int_0;
        frame_43258ceec97c7d5be3d32fc0d5435667->m_frame.f_lineno = 7;
        tmp_import_name_from_2 = IMPORT_MODULE5(tstate, tmp_name_value_4, tmp_globals_arg_value_4, tmp_locals_arg_value_4, tmp_fromlist_value_4, tmp_level_value_4);
        if (tmp_import_name_from_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 7;

            goto frame_exception_exit_1;
        }
        if (PyModule_Check(tmp_import_name_from_2)) {
            tmp_assign_source_8 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_2,
                (PyObject *)moduledict_piexif$_insert,
                mod_consts[29],
                const_int_0
            );
        } else {
            tmp_assign_source_8 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_2, mod_consts[29]);
        }

        Py_DECREF(tmp_import_name_from_2);
        if (tmp_assign_source_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 7;

            goto frame_exception_exit_1;
        }
        UPDATE_STRING_DICT1(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[29], tmp_assign_source_8);
    }


    // Put the previous frame back on top.
    popFrameStack(tstate);

    goto frame_no_exception_1;
    frame_exception_exit_1:


    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_43258ceec97c7d5be3d32fc0d5435667, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        } else if (exception_tb->tb_frame != &frame_43258ceec97c7d5be3d32fc0d5435667->m_frame) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_43258ceec97c7d5be3d32fc0d5435667, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        }
    }



    assertFrameObject(frame_43258ceec97c7d5be3d32fc0d5435667);

    // Put the previous frame back on top.
    popFrameStack(tstate);

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_1:;
    {
        PyObject *tmp_assign_source_9;
        PyObject *tmp_defaults_1;
        tmp_defaults_1 = mod_consts[54];
        Py_INCREF(tmp_defaults_1);


        tmp_assign_source_9 = MAKE_FUNCTION_piexif$_insert$$$function__1_insert(tmp_defaults_1);

        UPDATE_STRING_DICT1(moduledict_piexif$_insert, (Nuitka_StringObject *)mod_consts[30], tmp_assign_source_9);
    }

    // Report to PGO about leaving the module without error.
    PGO_onModuleExit("piexif$_insert", false);

#if defined(_NUITKA_MODULE) && 0
    {
        PyObject *post_load = IMPORT_EMBEDDED_MODULE(tstate, "piexif._insert" "-postLoad");
        if (post_load == NULL) {
            return NULL;
        }
    }
#endif

    Py_INCREF(module_piexif$_insert);
    return module_piexif$_insert;
    module_exception_exit:

#if defined(_NUITKA_MODULE) && 0
    {
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_piexif$_insert, (Nuitka_StringObject *)const_str_plain___name__);

        if (module_name != NULL) {
            Nuitka_DelModule(tstate, module_name);
        }
    }
#endif
    PGO_onModuleExit("piexif$_insert", false);

    RESTORE_ERROR_OCCURRED_STATE(tstate, &exception_state);
    return NULL;
}
