/* Generated code for Python module 'qtimgren$ui_profiles'
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

/* The "module_qtimgren$ui_profiles" is a Python object pointer of module type.
 *
 * Note: For full compatibility with CPython, every module variable access
 * needs to go through it except for cases where the module cannot possibly
 * have changed in the mean time.
 */

PyObject *module_qtimgren$ui_profiles;
PyDictObject *moduledict_qtimgren$ui_profiles;

/* The declarations of module constants used, if any. */
static PyObject *mod_consts[115];
#ifndef __NUITKA_NO_ASSERT__
static Py_hash_t mod_consts_hash[115];
#endif

static PyObject *module_filename_obj = NULL;

/* Indicator if this modules private constants were created yet. */
static bool constants_created = false;

/* Function to create module private constants. */
static void createModuleConstants(PyThreadState *tstate) {
    if (constants_created == false) {
        loadConstantsBlob(tstate, &mod_consts[0], UN_TRANSLATE("qtimgren.ui_profiles"));
        constants_created = true;

#ifndef __NUITKA_NO_ASSERT__
        for (int i = 0; i < 115; i++) {
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
void checkModuleConstants_qtimgren$ui_profiles(PyThreadState *tstate) {
    // The module may not have been used at all, then ignore this.
    if (constants_created == false) return;

    for (int i = 0; i < 115; i++) {
        assert(mod_consts_hash[i] == DEEP_HASH(tstate, mod_consts[i]));
        CHECK_OBJECT_DEEP(mod_consts[i]);
    }
}
#endif

// Helper to preserving module variables for Python3.11+
#if 9
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
static PyObject *module_var_accessor_qtimgren$ui_profiles_$$_QAbstractItemView(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_qtimgren$ui_profiles->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_qtimgren$ui_profiles->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[19]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_qtimgren$ui_profiles->ma_keys;
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
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[19]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[19]);
    }

    return result;
}

static PyObject *module_var_accessor_qtimgren$ui_profiles_$$_QCoreApplication(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_qtimgren$ui_profiles->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_qtimgren$ui_profiles->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[43]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_qtimgren$ui_profiles->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[43])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[43], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[43])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[43], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[43]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[43]);
    }

    return result;
}

static PyObject *module_var_accessor_qtimgren$ui_profiles_$$_QDialogButtonBox(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_qtimgren$ui_profiles->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_qtimgren$ui_profiles->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[30]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_qtimgren$ui_profiles->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[30])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[30], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[30])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[30], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[30]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[30]);
    }

    return result;
}

static PyObject *module_var_accessor_qtimgren$ui_profiles_$$_QHBoxLayout(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_qtimgren$ui_profiles->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_qtimgren$ui_profiles->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[7]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_qtimgren$ui_profiles->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[7])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[7], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[7])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[7], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[7]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[7]);
    }

    return result;
}

static PyObject *module_var_accessor_qtimgren$ui_profiles_$$_QMetaObject(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_qtimgren$ui_profiles->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_qtimgren$ui_profiles->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[40]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_qtimgren$ui_profiles->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[40])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[40], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[40])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[40], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[40]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[40]);
    }

    return result;
}

static PyObject *module_var_accessor_qtimgren$ui_profiles_$$_QPushButton(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_qtimgren$ui_profiles->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_qtimgren$ui_profiles->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[24]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_qtimgren$ui_profiles->ma_keys;
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
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[24]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[24]);
    }

    return result;
}

static PyObject *module_var_accessor_qtimgren$ui_profiles_$$_QTableView(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_qtimgren$ui_profiles->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_qtimgren$ui_profiles->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[15]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_qtimgren$ui_profiles->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[15])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[15], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[15])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[15], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[15]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[15]);
    }

    return result;
}

static PyObject *module_var_accessor_qtimgren$ui_profiles_$$_QVBoxLayout(PyThreadState *tstate) {
#if 1
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_qtimgren$ui_profiles->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_qtimgren$ui_profiles->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[10]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_qtimgren$ui_profiles->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[10])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[10], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[10])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[10], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[10]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[10]);
    }

    return result;
}

static PyObject *module_var_accessor_qtimgren$ui_profiles_$$___spec__(PyThreadState *tstate) {
#if 0
    PyObject *result;

#if PYTHON_VERSION < 0x3b0
    static uint64_t dict_version = 0;
    static PyObject *cache_value = NULL;

    if (moduledict_qtimgren$ui_profiles->ma_version_tag == dict_version) {
        CHECK_OBJECT_X(cache_value);
        result = cache_value;
    } else {
        dict_version = moduledict_qtimgren$ui_profiles->ma_version_tag;

        result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[114]);
        cache_value = result;
    }
#else
    static uint32_t dict_keys_version = 0xFFFFFFFF;
    static Py_ssize_t cache_dk_index = 0;

    PyDictKeysObject *dk = moduledict_qtimgren$ui_profiles->ma_keys;
    assert(DK_IS_UNICODE(dk));

#if PYTHON_VERSION >= 0x3c0
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(tstate->interp, dk);
#else
    uint32_t current_dk_version = _Nuitka_PyDictKeys_GetVersionForCurrentState(dk);
#endif

    if (current_dk_version != dict_keys_version) {
        dict_keys_version = current_dk_version;
        Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[114])->_base._base.hash;
        assert(hash != -1);

        cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[114], hash);
    }

    if (cache_dk_index >= 0) {
        assert(dk->dk_kind != DICT_KEYS_SPLIT);

        PyDictUnicodeEntry *entries = DK_UNICODE_ENTRIES(dk);

        result = entries[cache_dk_index].me_value;

        if (unlikely(result == NULL)) {
            Py_hash_t hash = ((Nuitka_StringObject *)mod_consts[114])->_base._base.hash;
            assert(hash != -1);

            cache_dk_index = Nuitka_Py_unicodekeys_lookup_unicode(dk, mod_consts[114], hash);

            if (cache_dk_index >= 0) {
                result = entries[cache_dk_index].me_value;
            }
        }
    } else {
        result = NULL;
    }
#endif

#else
    PyObject *result = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[114]);
#endif

    if (unlikely(result == NULL)) {
        result = GET_STRING_DICT_VALUE(dict_builtin, (Nuitka_StringObject *)mod_consts[114]);
    }

    return result;
}


// The module code objects.
static PyCodeObject *code_objects_5292643c84c58ca7ae9bb7bed7e3ceed;
static PyCodeObject *code_objects_a87da0f363d9e00c30155fc19acc845d;
static PyCodeObject *code_objects_4a788d4b1316fa0c0d7ebed1b52367c4;
static PyCodeObject *code_objects_16b17377e50f407262c01bd6e73a0afa;

static void createModuleCodeObjects(void) {
    module_filename_obj = MAKE_RELATIVE_PATH(mod_consts[109]); CHECK_OBJECT(module_filename_obj);
    code_objects_5292643c84c58ca7ae9bb7bed7e3ceed = MAKE_CODE_OBJECT(module_filename_obj, 1, CO_NOFREE, mod_consts[110], mod_consts[110], NULL, NULL, 0, 0, 0);
    code_objects_a87da0f363d9e00c30155fc19acc845d = MAKE_CODE_OBJECT(module_filename_obj, 22, CO_NOFREE, mod_consts[97], mod_consts[97], mod_consts[111], NULL, 0, 0, 0);
    code_objects_4a788d4b1316fa0c0d7ebed1b52367c4 = MAKE_CODE_OBJECT(module_filename_obj, 74, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE, mod_consts[36], mod_consts[107], mod_consts[112], NULL, 2, 0, 0);
    code_objects_16b17377e50f407262c01bd6e73a0afa = MAKE_CODE_OBJECT(module_filename_obj, 23, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE, mod_consts[105], mod_consts[106], mod_consts[112], NULL, 2, 0, 0);
}

// The module function declarations.
NUITKA_CROSS_MODULE PyObject *impl_qtimgren$__main__$$$helper_function__mro_entries_conversion(PyThreadState *tstate, PyObject **python_pars);


static PyObject *MAKE_FUNCTION_qtimgren$ui_profiles$$$function__1_setupUi();


static PyObject *MAKE_FUNCTION_qtimgren$ui_profiles$$$function__2_retranslateUi();


// The module function definitions.
static PyObject *impl_qtimgren$ui_profiles$$$function__1_setupUi(PyThreadState *tstate, struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = HAS_ERROR_OCCURRED(tstate);
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_profiles = python_pars[1];
    struct Nuitka_FrameObject *frame_16b17377e50f407262c01bd6e73a0afa;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    struct Nuitka_ExceptionPreservationItem exception_state = Empty_Nuitka_ExceptionPreservationItem;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    int tmp_res;
    NUITKA_MAY_BE_UNUSED nuitka_void tmp_unused;
    bool tmp_result;
    static struct Nuitka_FrameObject *cache_frame_16b17377e50f407262c01bd6e73a0afa = NULL;
    PyObject *tmp_return_value = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_16b17377e50f407262c01bd6e73a0afa)) {
        Py_XDECREF(cache_frame_16b17377e50f407262c01bd6e73a0afa);

#if _DEBUG_REFCOUNTS
        if (cache_frame_16b17377e50f407262c01bd6e73a0afa == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_16b17377e50f407262c01bd6e73a0afa = MAKE_FUNCTION_FRAME(tstate, code_objects_16b17377e50f407262c01bd6e73a0afa, module_qtimgren$ui_profiles, sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_16b17377e50f407262c01bd6e73a0afa->m_type_description == NULL);
    frame_16b17377e50f407262c01bd6e73a0afa = cache_frame_16b17377e50f407262c01bd6e73a0afa;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(tstate, frame_16b17377e50f407262c01bd6e73a0afa);
    assert(Py_REFCNT(frame_16b17377e50f407262c01bd6e73a0afa) == 2);

    // Framed code:
    {
        bool tmp_condition_result_1;
        PyObject *tmp_operand_value_1;
        PyObject *tmp_called_instance_1;
        CHECK_OBJECT(par_profiles);
        tmp_called_instance_1 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 24;
        tmp_operand_value_1 = CALL_METHOD_NO_ARGS(tstate, tmp_called_instance_1, mod_consts[0]);
        if (tmp_operand_value_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 24;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_res = CHECK_IF_TRUE(tmp_operand_value_1);
        Py_DECREF(tmp_operand_value_1);
        if (tmp_res == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 24;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_condition_result_1 = (tmp_res == 0) ? true : false;
        if (tmp_condition_result_1 != false) {
            goto branch_yes_1;
        } else {
            goto branch_no_1;
        }
    }
    branch_yes_1:;
    {
        PyObject *tmp_called_instance_2;
        PyObject *tmp_call_result_1;
        CHECK_OBJECT(par_profiles);
        tmp_called_instance_2 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 25;
        tmp_call_result_1 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_2,
            mod_consts[1],
            PyTuple_GET_ITEM(mod_consts[2], 0)
        );

        if (tmp_call_result_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 25;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_1);
    }
    branch_no_1:;
    {
        PyObject *tmp_called_instance_3;
        PyObject *tmp_call_result_2;
        CHECK_OBJECT(par_profiles);
        tmp_called_instance_3 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 26;
        tmp_call_result_2 = CALL_METHOD_WITH_ARGS2(
            tstate,
            tmp_called_instance_3,
            mod_consts[3],
            &PyTuple_GET_ITEM(mod_consts[4], 0)
        );

        if (tmp_call_result_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 26;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_2);
    }
    {
        PyObject *tmp_called_instance_4;
        PyObject *tmp_call_result_3;
        CHECK_OBJECT(par_profiles);
        tmp_called_instance_4 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 27;
        tmp_call_result_3 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_4,
            mod_consts[5],
            PyTuple_GET_ITEM(mod_consts[6], 0)
        );

        if (tmp_call_result_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 27;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_3);
    }
    {
        PyObject *tmp_assattr_value_1;
        PyObject *tmp_called_value_1;
        PyObject *tmp_args_element_value_1;
        PyObject *tmp_assattr_target_1;
        tmp_called_value_1 = module_var_accessor_qtimgren$ui_profiles_$$_QHBoxLayout(tstate);
        if (unlikely(tmp_called_value_1 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[7]);
        }

        if (tmp_called_value_1 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 28;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_profiles);
        tmp_args_element_value_1 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 28;
        tmp_assattr_value_1 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_1, tmp_args_element_value_1);
        if (tmp_assattr_value_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 28;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_assattr_target_1 = par_self;
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_1, mod_consts[8], tmp_assattr_value_1);
        Py_DECREF(tmp_assattr_value_1);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 28;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_called_instance_5;
        PyObject *tmp_expression_value_1;
        PyObject *tmp_call_result_4;
        CHECK_OBJECT(par_self);
        tmp_expression_value_1 = par_self;
        tmp_called_instance_5 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_1, mod_consts[8]);
        if (tmp_called_instance_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 29;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 29;
        tmp_call_result_4 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_5,
            mod_consts[1],
            PyTuple_GET_ITEM(mod_consts[9], 0)
        );

        Py_DECREF(tmp_called_instance_5);
        if (tmp_call_result_4 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 29;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_4);
    }
    {
        PyObject *tmp_assattr_value_2;
        PyObject *tmp_called_value_2;
        PyObject *tmp_assattr_target_2;
        tmp_called_value_2 = module_var_accessor_qtimgren$ui_profiles_$$_QVBoxLayout(tstate);
        if (unlikely(tmp_called_value_2 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[10]);
        }

        if (tmp_called_value_2 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 30;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 30;
        tmp_assattr_value_2 = CALL_FUNCTION_NO_ARGS(tstate, tmp_called_value_2);
        if (tmp_assattr_value_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 30;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_assattr_target_2 = par_self;
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_2, mod_consts[11], tmp_assattr_value_2);
        Py_DECREF(tmp_assattr_value_2);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 30;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_called_instance_6;
        PyObject *tmp_expression_value_2;
        PyObject *tmp_call_result_5;
        CHECK_OBJECT(par_self);
        tmp_expression_value_2 = par_self;
        tmp_called_instance_6 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_2, mod_consts[11]);
        if (tmp_called_instance_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 31;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 31;
        tmp_call_result_5 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_6,
            mod_consts[1],
            PyTuple_GET_ITEM(mod_consts[12], 0)
        );

        Py_DECREF(tmp_called_instance_6);
        if (tmp_call_result_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 31;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_5);
    }
    {
        PyObject *tmp_assattr_value_3;
        PyObject *tmp_called_value_3;
        PyObject *tmp_assattr_target_3;
        tmp_called_value_3 = module_var_accessor_qtimgren$ui_profiles_$$_QHBoxLayout(tstate);
        if (unlikely(tmp_called_value_3 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[7]);
        }

        if (tmp_called_value_3 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 32;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 32;
        tmp_assattr_value_3 = CALL_FUNCTION_NO_ARGS(tstate, tmp_called_value_3);
        if (tmp_assattr_value_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 32;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_assattr_target_3 = par_self;
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_3, mod_consts[13], tmp_assattr_value_3);
        Py_DECREF(tmp_assattr_value_3);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 32;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_called_instance_7;
        PyObject *tmp_expression_value_3;
        PyObject *tmp_call_result_6;
        CHECK_OBJECT(par_self);
        tmp_expression_value_3 = par_self;
        tmp_called_instance_7 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_3, mod_consts[13]);
        if (tmp_called_instance_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 33;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 33;
        tmp_call_result_6 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_7,
            mod_consts[1],
            PyTuple_GET_ITEM(mod_consts[14], 0)
        );

        Py_DECREF(tmp_called_instance_7);
        if (tmp_call_result_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 33;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_6);
    }
    {
        PyObject *tmp_assattr_value_4;
        PyObject *tmp_called_value_4;
        PyObject *tmp_args_element_value_2;
        PyObject *tmp_assattr_target_4;
        tmp_called_value_4 = module_var_accessor_qtimgren$ui_profiles_$$_QTableView(tstate);
        if (unlikely(tmp_called_value_4 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[15]);
        }

        if (tmp_called_value_4 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 34;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_profiles);
        tmp_args_element_value_2 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 34;
        tmp_assattr_value_4 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_4, tmp_args_element_value_2);
        if (tmp_assattr_value_4 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 34;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_assattr_target_4 = par_self;
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_4, mod_consts[16], tmp_assattr_value_4);
        Py_DECREF(tmp_assattr_value_4);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 34;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_called_instance_8;
        PyObject *tmp_expression_value_4;
        PyObject *tmp_call_result_7;
        CHECK_OBJECT(par_self);
        tmp_expression_value_4 = par_self;
        tmp_called_instance_8 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_4, mod_consts[16]);
        if (tmp_called_instance_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 35;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 35;
        tmp_call_result_7 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_8,
            mod_consts[1],
            PyTuple_GET_ITEM(mod_consts[17], 0)
        );

        Py_DECREF(tmp_called_instance_8);
        if (tmp_call_result_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 35;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_7);
    }
    {
        PyObject *tmp_called_value_5;
        PyObject *tmp_expression_value_5;
        PyObject *tmp_expression_value_6;
        PyObject *tmp_call_result_8;
        PyObject *tmp_args_element_value_3;
        PyObject *tmp_expression_value_7;
        CHECK_OBJECT(par_self);
        tmp_expression_value_6 = par_self;
        tmp_expression_value_5 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_6, mod_consts[16]);
        if (tmp_expression_value_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 36;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_5 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_5, mod_consts[18]);
        Py_DECREF(tmp_expression_value_5);
        if (tmp_called_value_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 36;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_expression_value_7 = module_var_accessor_qtimgren$ui_profiles_$$_QAbstractItemView(tstate);
        if (unlikely(tmp_expression_value_7 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[19]);
        }

        if (tmp_expression_value_7 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_5);

            exception_lineno = 36;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_args_element_value_3 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_7, mod_consts[20]);
        if (tmp_args_element_value_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_5);

            exception_lineno = 36;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 36;
        tmp_call_result_8 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_5, tmp_args_element_value_3);
        Py_DECREF(tmp_called_value_5);
        Py_DECREF(tmp_args_element_value_3);
        if (tmp_call_result_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 36;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_8);
    }
    {
        PyObject *tmp_called_value_6;
        PyObject *tmp_expression_value_8;
        PyObject *tmp_expression_value_9;
        PyObject *tmp_call_result_9;
        PyObject *tmp_args_element_value_4;
        PyObject *tmp_expression_value_10;
        CHECK_OBJECT(par_self);
        tmp_expression_value_9 = par_self;
        tmp_expression_value_8 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_9, mod_consts[13]);
        if (tmp_expression_value_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 38;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_6 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_8, mod_consts[21]);
        Py_DECREF(tmp_expression_value_8);
        if (tmp_called_value_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 38;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_expression_value_10 = par_self;
        tmp_args_element_value_4 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_10, mod_consts[16]);
        if (tmp_args_element_value_4 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_6);

            exception_lineno = 38;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 38;
        tmp_call_result_9 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_6, tmp_args_element_value_4);
        Py_DECREF(tmp_called_value_6);
        Py_DECREF(tmp_args_element_value_4);
        if (tmp_call_result_9 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 38;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_9);
    }
    {
        PyObject *tmp_assattr_value_5;
        PyObject *tmp_called_value_7;
        PyObject *tmp_assattr_target_5;
        tmp_called_value_7 = module_var_accessor_qtimgren$ui_profiles_$$_QVBoxLayout(tstate);
        if (unlikely(tmp_called_value_7 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[10]);
        }

        if (tmp_called_value_7 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 40;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 40;
        tmp_assattr_value_5 = CALL_FUNCTION_NO_ARGS(tstate, tmp_called_value_7);
        if (tmp_assattr_value_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 40;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_assattr_target_5 = par_self;
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_5, mod_consts[22], tmp_assattr_value_5);
        Py_DECREF(tmp_assattr_value_5);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 40;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_called_instance_9;
        PyObject *tmp_expression_value_11;
        PyObject *tmp_call_result_10;
        CHECK_OBJECT(par_self);
        tmp_expression_value_11 = par_self;
        tmp_called_instance_9 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_11, mod_consts[22]);
        if (tmp_called_instance_9 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 41;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 41;
        tmp_call_result_10 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_9,
            mod_consts[1],
            PyTuple_GET_ITEM(mod_consts[23], 0)
        );

        Py_DECREF(tmp_called_instance_9);
        if (tmp_call_result_10 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 41;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_10);
    }
    {
        PyObject *tmp_assattr_value_6;
        PyObject *tmp_called_value_8;
        PyObject *tmp_args_element_value_5;
        PyObject *tmp_assattr_target_6;
        tmp_called_value_8 = module_var_accessor_qtimgren$ui_profiles_$$_QPushButton(tstate);
        if (unlikely(tmp_called_value_8 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[24]);
        }

        if (tmp_called_value_8 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 42;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_profiles);
        tmp_args_element_value_5 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 42;
        tmp_assattr_value_6 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_8, tmp_args_element_value_5);
        if (tmp_assattr_value_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 42;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_assattr_target_6 = par_self;
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_6, mod_consts[25], tmp_assattr_value_6);
        Py_DECREF(tmp_assattr_value_6);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 42;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_called_instance_10;
        PyObject *tmp_expression_value_12;
        PyObject *tmp_call_result_11;
        CHECK_OBJECT(par_self);
        tmp_expression_value_12 = par_self;
        tmp_called_instance_10 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_12, mod_consts[25]);
        if (tmp_called_instance_10 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 43;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 43;
        tmp_call_result_11 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_10,
            mod_consts[1],
            PyTuple_GET_ITEM(mod_consts[26], 0)
        );

        Py_DECREF(tmp_called_instance_10);
        if (tmp_call_result_11 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 43;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_11);
    }
    {
        PyObject *tmp_called_value_9;
        PyObject *tmp_expression_value_13;
        PyObject *tmp_expression_value_14;
        PyObject *tmp_call_result_12;
        PyObject *tmp_args_element_value_6;
        PyObject *tmp_expression_value_15;
        CHECK_OBJECT(par_self);
        tmp_expression_value_14 = par_self;
        tmp_expression_value_13 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_14, mod_consts[22]);
        if (tmp_expression_value_13 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 45;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_9 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_13, mod_consts[21]);
        Py_DECREF(tmp_expression_value_13);
        if (tmp_called_value_9 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 45;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_expression_value_15 = par_self;
        tmp_args_element_value_6 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_15, mod_consts[25]);
        if (tmp_args_element_value_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_9);

            exception_lineno = 45;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 45;
        tmp_call_result_12 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_9, tmp_args_element_value_6);
        Py_DECREF(tmp_called_value_9);
        Py_DECREF(tmp_args_element_value_6);
        if (tmp_call_result_12 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 45;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_12);
    }
    {
        PyObject *tmp_assattr_value_7;
        PyObject *tmp_called_value_10;
        PyObject *tmp_args_element_value_7;
        PyObject *tmp_assattr_target_7;
        tmp_called_value_10 = module_var_accessor_qtimgren$ui_profiles_$$_QPushButton(tstate);
        if (unlikely(tmp_called_value_10 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[24]);
        }

        if (tmp_called_value_10 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 47;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_profiles);
        tmp_args_element_value_7 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 47;
        tmp_assattr_value_7 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_10, tmp_args_element_value_7);
        if (tmp_assattr_value_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 47;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_assattr_target_7 = par_self;
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_7, mod_consts[27], tmp_assattr_value_7);
        Py_DECREF(tmp_assattr_value_7);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 47;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_called_instance_11;
        PyObject *tmp_expression_value_16;
        PyObject *tmp_call_result_13;
        CHECK_OBJECT(par_self);
        tmp_expression_value_16 = par_self;
        tmp_called_instance_11 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_16, mod_consts[27]);
        if (tmp_called_instance_11 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 48;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 48;
        tmp_call_result_13 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_11,
            mod_consts[1],
            PyTuple_GET_ITEM(mod_consts[28], 0)
        );

        Py_DECREF(tmp_called_instance_11);
        if (tmp_call_result_13 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 48;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_13);
    }
    {
        PyObject *tmp_called_value_11;
        PyObject *tmp_expression_value_17;
        PyObject *tmp_expression_value_18;
        PyObject *tmp_call_result_14;
        PyObject *tmp_args_element_value_8;
        PyObject *tmp_expression_value_19;
        CHECK_OBJECT(par_self);
        tmp_expression_value_18 = par_self;
        tmp_expression_value_17 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_18, mod_consts[22]);
        if (tmp_expression_value_17 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 50;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_11 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_17, mod_consts[21]);
        Py_DECREF(tmp_expression_value_17);
        if (tmp_called_value_11 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 50;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_expression_value_19 = par_self;
        tmp_args_element_value_8 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_19, mod_consts[27]);
        if (tmp_args_element_value_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_11);

            exception_lineno = 50;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 50;
        tmp_call_result_14 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_11, tmp_args_element_value_8);
        Py_DECREF(tmp_called_value_11);
        Py_DECREF(tmp_args_element_value_8);
        if (tmp_call_result_14 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 50;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_14);
    }
    {
        PyObject *tmp_called_value_12;
        PyObject *tmp_expression_value_20;
        PyObject *tmp_expression_value_21;
        PyObject *tmp_call_result_15;
        PyObject *tmp_args_element_value_9;
        PyObject *tmp_expression_value_22;
        CHECK_OBJECT(par_self);
        tmp_expression_value_21 = par_self;
        tmp_expression_value_20 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_21, mod_consts[13]);
        if (tmp_expression_value_20 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 53;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_12 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_20, mod_consts[29]);
        Py_DECREF(tmp_expression_value_20);
        if (tmp_called_value_12 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 53;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_expression_value_22 = par_self;
        tmp_args_element_value_9 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_22, mod_consts[22]);
        if (tmp_args_element_value_9 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_12);

            exception_lineno = 53;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 53;
        tmp_call_result_15 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_12, tmp_args_element_value_9);
        Py_DECREF(tmp_called_value_12);
        Py_DECREF(tmp_args_element_value_9);
        if (tmp_call_result_15 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 53;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_15);
    }
    {
        PyObject *tmp_called_value_13;
        PyObject *tmp_expression_value_23;
        PyObject *tmp_expression_value_24;
        PyObject *tmp_call_result_16;
        PyObject *tmp_args_element_value_10;
        PyObject *tmp_expression_value_25;
        CHECK_OBJECT(par_self);
        tmp_expression_value_24 = par_self;
        tmp_expression_value_23 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_24, mod_consts[11]);
        if (tmp_expression_value_23 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 56;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_13 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_23, mod_consts[29]);
        Py_DECREF(tmp_expression_value_23);
        if (tmp_called_value_13 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 56;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_expression_value_25 = par_self;
        tmp_args_element_value_10 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_25, mod_consts[13]);
        if (tmp_args_element_value_10 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_13);

            exception_lineno = 56;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 56;
        tmp_call_result_16 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_13, tmp_args_element_value_10);
        Py_DECREF(tmp_called_value_13);
        Py_DECREF(tmp_args_element_value_10);
        if (tmp_call_result_16 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 56;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_16);
    }
    {
        PyObject *tmp_assattr_value_8;
        PyObject *tmp_called_value_14;
        PyObject *tmp_args_element_value_11;
        PyObject *tmp_assattr_target_8;
        tmp_called_value_14 = module_var_accessor_qtimgren$ui_profiles_$$_QDialogButtonBox(tstate);
        if (unlikely(tmp_called_value_14 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[30]);
        }

        if (tmp_called_value_14 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 58;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_profiles);
        tmp_args_element_value_11 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 58;
        tmp_assattr_value_8 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_14, tmp_args_element_value_11);
        if (tmp_assattr_value_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 58;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_assattr_target_8 = par_self;
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_8, mod_consts[31], tmp_assattr_value_8);
        Py_DECREF(tmp_assattr_value_8);
        if (tmp_result == false) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 58;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_called_instance_12;
        PyObject *tmp_expression_value_26;
        PyObject *tmp_call_result_17;
        CHECK_OBJECT(par_self);
        tmp_expression_value_26 = par_self;
        tmp_called_instance_12 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_26, mod_consts[31]);
        if (tmp_called_instance_12 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 59;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 59;
        tmp_call_result_17 = CALL_METHOD_WITH_SINGLE_ARG(
            tstate,
            tmp_called_instance_12,
            mod_consts[1],
            PyTuple_GET_ITEM(mod_consts[32], 0)
        );

        Py_DECREF(tmp_called_instance_12);
        if (tmp_call_result_17 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 59;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_17);
    }
    {
        PyObject *tmp_called_value_15;
        PyObject *tmp_expression_value_27;
        PyObject *tmp_expression_value_28;
        PyObject *tmp_call_result_18;
        PyObject *tmp_args_element_value_12;
        PyObject *tmp_bitor_expr_left_1;
        PyObject *tmp_bitor_expr_right_1;
        PyObject *tmp_expression_value_29;
        PyObject *tmp_expression_value_30;
        CHECK_OBJECT(par_self);
        tmp_expression_value_28 = par_self;
        tmp_expression_value_27 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_28, mod_consts[31]);
        if (tmp_expression_value_27 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 60;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_15 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_27, mod_consts[33]);
        Py_DECREF(tmp_expression_value_27);
        if (tmp_called_value_15 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 60;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_expression_value_29 = module_var_accessor_qtimgren$ui_profiles_$$_QDialogButtonBox(tstate);
        if (unlikely(tmp_expression_value_29 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[30]);
        }

        if (tmp_expression_value_29 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_15);

            exception_lineno = 60;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_bitor_expr_left_1 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_29, mod_consts[34]);
        if (tmp_bitor_expr_left_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_15);

            exception_lineno = 60;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_expression_value_30 = module_var_accessor_qtimgren$ui_profiles_$$_QDialogButtonBox(tstate);
        if (unlikely(tmp_expression_value_30 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[30]);
        }

        if (tmp_expression_value_30 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_15);
            Py_DECREF(tmp_bitor_expr_left_1);

            exception_lineno = 60;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_bitor_expr_right_1 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_30, mod_consts[35]);
        if (tmp_bitor_expr_right_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_15);
            Py_DECREF(tmp_bitor_expr_left_1);

            exception_lineno = 60;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_args_element_value_12 = BINARY_OPERATION_BITOR_OBJECT_OBJECT_OBJECT(tmp_bitor_expr_left_1, tmp_bitor_expr_right_1);
        Py_DECREF(tmp_bitor_expr_left_1);
        Py_DECREF(tmp_bitor_expr_right_1);
        if (tmp_args_element_value_12 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_15);

            exception_lineno = 60;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 60;
        tmp_call_result_18 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_15, tmp_args_element_value_12);
        Py_DECREF(tmp_called_value_15);
        Py_DECREF(tmp_args_element_value_12);
        if (tmp_call_result_18 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 60;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_18);
    }
    {
        PyObject *tmp_called_value_16;
        PyObject *tmp_expression_value_31;
        PyObject *tmp_expression_value_32;
        PyObject *tmp_call_result_19;
        PyObject *tmp_args_element_value_13;
        PyObject *tmp_expression_value_33;
        CHECK_OBJECT(par_self);
        tmp_expression_value_32 = par_self;
        tmp_expression_value_31 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_32, mod_consts[11]);
        if (tmp_expression_value_31 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 62;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_16 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_31, mod_consts[21]);
        Py_DECREF(tmp_expression_value_31);
        if (tmp_called_value_16 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 62;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_expression_value_33 = par_self;
        tmp_args_element_value_13 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_33, mod_consts[31]);
        if (tmp_args_element_value_13 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_16);

            exception_lineno = 62;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 62;
        tmp_call_result_19 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_16, tmp_args_element_value_13);
        Py_DECREF(tmp_called_value_16);
        Py_DECREF(tmp_args_element_value_13);
        if (tmp_call_result_19 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 62;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_19);
    }
    {
        PyObject *tmp_called_value_17;
        PyObject *tmp_expression_value_34;
        PyObject *tmp_expression_value_35;
        PyObject *tmp_call_result_20;
        PyObject *tmp_args_element_value_14;
        PyObject *tmp_expression_value_36;
        CHECK_OBJECT(par_self);
        tmp_expression_value_35 = par_self;
        tmp_expression_value_34 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_35, mod_consts[8]);
        if (tmp_expression_value_34 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 65;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_17 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_34, mod_consts[29]);
        Py_DECREF(tmp_expression_value_34);
        if (tmp_called_value_17 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 65;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_self);
        tmp_expression_value_36 = par_self;
        tmp_args_element_value_14 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_36, mod_consts[11]);
        if (tmp_args_element_value_14 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_17);

            exception_lineno = 65;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 65;
        tmp_call_result_20 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_17, tmp_args_element_value_14);
        Py_DECREF(tmp_called_value_17);
        Py_DECREF(tmp_args_element_value_14);
        if (tmp_call_result_20 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 65;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_20);
    }
    {
        PyObject *tmp_called_instance_13;
        PyObject *tmp_call_result_21;
        PyObject *tmp_args_element_value_15;
        CHECK_OBJECT(par_self);
        tmp_called_instance_13 = par_self;
        CHECK_OBJECT(par_profiles);
        tmp_args_element_value_15 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 68;
        tmp_call_result_21 = CALL_METHOD_WITH_SINGLE_ARG(tstate, tmp_called_instance_13, mod_consts[36], tmp_args_element_value_15);
        if (tmp_call_result_21 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 68;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_21);
    }
    {
        PyObject *tmp_called_value_18;
        PyObject *tmp_expression_value_37;
        PyObject *tmp_expression_value_38;
        PyObject *tmp_expression_value_39;
        PyObject *tmp_call_result_22;
        PyObject *tmp_args_element_value_16;
        PyObject *tmp_expression_value_40;
        CHECK_OBJECT(par_self);
        tmp_expression_value_39 = par_self;
        tmp_expression_value_38 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_39, mod_consts[31]);
        if (tmp_expression_value_38 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 69;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_expression_value_37 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_38, mod_consts[37]);
        Py_DECREF(tmp_expression_value_38);
        if (tmp_expression_value_37 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 69;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_18 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_37, mod_consts[38]);
        Py_DECREF(tmp_expression_value_37);
        if (tmp_called_value_18 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 69;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_profiles);
        tmp_expression_value_40 = par_profiles;
        tmp_args_element_value_16 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_40, mod_consts[39]);
        if (tmp_args_element_value_16 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_18);

            exception_lineno = 69;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 69;
        tmp_call_result_22 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_18, tmp_args_element_value_16);
        Py_DECREF(tmp_called_value_18);
        Py_DECREF(tmp_args_element_value_16);
        if (tmp_call_result_22 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 69;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_22);
    }
    {
        PyObject *tmp_called_instance_14;
        PyObject *tmp_call_result_23;
        PyObject *tmp_args_element_value_17;
        tmp_called_instance_14 = module_var_accessor_qtimgren$ui_profiles_$$_QMetaObject(tstate);
        if (unlikely(tmp_called_instance_14 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[40]);
        }

        if (tmp_called_instance_14 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));



            exception_lineno = 71;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_profiles);
        tmp_args_element_value_17 = par_profiles;
        frame_16b17377e50f407262c01bd6e73a0afa->m_frame.f_lineno = 71;
        tmp_call_result_23 = CALL_METHOD_WITH_SINGLE_ARG(tstate, tmp_called_instance_14, mod_consts[41], tmp_args_element_value_17);
        if (tmp_call_result_23 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 71;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_23);
    }


    // Put the previous frame back on top.
    popFrameStack(tstate);

    goto frame_no_exception_1;
    frame_exception_exit_1:


    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_16b17377e50f407262c01bd6e73a0afa, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        } else if (exception_tb->tb_frame != &frame_16b17377e50f407262c01bd6e73a0afa->m_frame) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_16b17377e50f407262c01bd6e73a0afa, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        }
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_16b17377e50f407262c01bd6e73a0afa,
        type_description_1,
        par_self,
        par_profiles
    );


    // Release cached frame if used for exception.
    if (frame_16b17377e50f407262c01bd6e73a0afa == cache_frame_16b17377e50f407262c01bd6e73a0afa) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_16b17377e50f407262c01bd6e73a0afa);
        cache_frame_16b17377e50f407262c01bd6e73a0afa = NULL;
    }

    assertFrameObject(frame_16b17377e50f407262c01bd6e73a0afa);

    // Put the previous frame back on top.
    popFrameStack(tstate);

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;
    tmp_return_value = Py_None;
    Py_INCREF(tmp_return_value);
    goto function_return_exit;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_profiles);
    Py_DECREF(par_profiles);
    CHECK_EXCEPTION_STATE(&exception_state);
    RESTORE_ERROR_OCCURRED_STATE(tstate, &exception_state);

    return NULL;

function_return_exit:
   // Function cleanup code if any.
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_profiles);
    Py_DECREF(par_profiles);

   // Actual function exit with return value, making sure we did not make
   // the error status worse despite non-NULL return.
   CHECK_OBJECT(tmp_return_value);
   assert(had_error || !HAS_ERROR_OCCURRED(tstate));
   return tmp_return_value;
}


static PyObject *impl_qtimgren$ui_profiles$$$function__2_retranslateUi(PyThreadState *tstate, struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = HAS_ERROR_OCCURRED(tstate);
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_profiles = python_pars[1];
    struct Nuitka_FrameObject *frame_4a788d4b1316fa0c0d7ebed1b52367c4;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    NUITKA_MAY_BE_UNUSED nuitka_void tmp_unused;
    struct Nuitka_ExceptionPreservationItem exception_state = Empty_Nuitka_ExceptionPreservationItem;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_4a788d4b1316fa0c0d7ebed1b52367c4 = NULL;
    PyObject *tmp_return_value = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_4a788d4b1316fa0c0d7ebed1b52367c4)) {
        Py_XDECREF(cache_frame_4a788d4b1316fa0c0d7ebed1b52367c4);

#if _DEBUG_REFCOUNTS
        if (cache_frame_4a788d4b1316fa0c0d7ebed1b52367c4 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_4a788d4b1316fa0c0d7ebed1b52367c4 = MAKE_FUNCTION_FRAME(tstate, code_objects_4a788d4b1316fa0c0d7ebed1b52367c4, module_qtimgren$ui_profiles, sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_type_description == NULL);
    frame_4a788d4b1316fa0c0d7ebed1b52367c4 = cache_frame_4a788d4b1316fa0c0d7ebed1b52367c4;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(tstate, frame_4a788d4b1316fa0c0d7ebed1b52367c4);
    assert(Py_REFCNT(frame_4a788d4b1316fa0c0d7ebed1b52367c4) == 2);

    // Framed code:
    {
        PyObject *tmp_called_value_1;
        PyObject *tmp_expression_value_1;
        PyObject *tmp_call_result_1;
        PyObject *tmp_args_element_value_1;
        PyObject *tmp_called_value_2;
        PyObject *tmp_expression_value_2;
        CHECK_OBJECT(par_profiles);
        tmp_expression_value_1 = par_profiles;
        tmp_called_value_1 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_1, mod_consts[42]);
        if (tmp_called_value_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 75;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_expression_value_2 = module_var_accessor_qtimgren$ui_profiles_$$_QCoreApplication(tstate);
        if (unlikely(tmp_expression_value_2 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[43]);
        }

        if (tmp_expression_value_2 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_1);

            exception_lineno = 75;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_2 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_2, mod_consts[44]);
        if (tmp_called_value_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_1);

            exception_lineno = 75;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame.f_lineno = 75;
        tmp_args_element_value_1 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_2, mod_consts[45]);

        Py_DECREF(tmp_called_value_2);
        if (tmp_args_element_value_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_1);

            exception_lineno = 75;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame.f_lineno = 75;
        tmp_call_result_1 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_1, tmp_args_element_value_1);
        Py_DECREF(tmp_called_value_1);
        Py_DECREF(tmp_args_element_value_1);
        if (tmp_call_result_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 75;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_1);
    }
    {
        PyObject *tmp_called_value_3;
        PyObject *tmp_expression_value_3;
        PyObject *tmp_expression_value_4;
        PyObject *tmp_call_result_2;
        PyObject *tmp_args_element_value_2;
        PyObject *tmp_called_value_4;
        PyObject *tmp_expression_value_5;
        CHECK_OBJECT(par_self);
        tmp_expression_value_4 = par_self;
        tmp_expression_value_3 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_4, mod_consts[25]);
        if (tmp_expression_value_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 77;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_3 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_3, mod_consts[46]);
        Py_DECREF(tmp_expression_value_3);
        if (tmp_called_value_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 77;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_expression_value_5 = module_var_accessor_qtimgren$ui_profiles_$$_QCoreApplication(tstate);
        if (unlikely(tmp_expression_value_5 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[43]);
        }

        if (tmp_expression_value_5 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_3);

            exception_lineno = 77;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_4 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_5, mod_consts[44]);
        if (tmp_called_value_4 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_3);

            exception_lineno = 77;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame.f_lineno = 77;
        tmp_args_element_value_2 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_4, mod_consts[47]);

        Py_DECREF(tmp_called_value_4);
        if (tmp_args_element_value_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_3);

            exception_lineno = 77;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame.f_lineno = 77;
        tmp_call_result_2 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_3, tmp_args_element_value_2);
        Py_DECREF(tmp_called_value_3);
        Py_DECREF(tmp_args_element_value_2);
        if (tmp_call_result_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 77;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_2);
    }
    {
        PyObject *tmp_called_value_5;
        PyObject *tmp_expression_value_6;
        PyObject *tmp_expression_value_7;
        PyObject *tmp_call_result_3;
        PyObject *tmp_args_element_value_3;
        PyObject *tmp_called_value_6;
        PyObject *tmp_expression_value_8;
        CHECK_OBJECT(par_self);
        tmp_expression_value_7 = par_self;
        tmp_expression_value_6 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_7, mod_consts[25]);
        if (tmp_expression_value_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 79;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_5 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_6, mod_consts[48]);
        Py_DECREF(tmp_expression_value_6);
        if (tmp_called_value_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 79;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_expression_value_8 = module_var_accessor_qtimgren$ui_profiles_$$_QCoreApplication(tstate);
        if (unlikely(tmp_expression_value_8 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[43]);
        }

        if (tmp_expression_value_8 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_5);

            exception_lineno = 79;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_6 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_8, mod_consts[44]);
        if (tmp_called_value_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_5);

            exception_lineno = 79;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame.f_lineno = 79;
        tmp_args_element_value_3 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_6, mod_consts[49]);

        Py_DECREF(tmp_called_value_6);
        if (tmp_args_element_value_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_5);

            exception_lineno = 79;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame.f_lineno = 79;
        tmp_call_result_3 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_5, tmp_args_element_value_3);
        Py_DECREF(tmp_called_value_5);
        Py_DECREF(tmp_args_element_value_3);
        if (tmp_call_result_3 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 79;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_3);
    }
    {
        PyObject *tmp_called_value_7;
        PyObject *tmp_expression_value_9;
        PyObject *tmp_expression_value_10;
        PyObject *tmp_call_result_4;
        PyObject *tmp_args_element_value_4;
        PyObject *tmp_called_value_8;
        PyObject *tmp_expression_value_11;
        CHECK_OBJECT(par_self);
        tmp_expression_value_10 = par_self;
        tmp_expression_value_9 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_10, mod_consts[27]);
        if (tmp_expression_value_9 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 81;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_7 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_9, mod_consts[46]);
        Py_DECREF(tmp_expression_value_9);
        if (tmp_called_value_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 81;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_expression_value_11 = module_var_accessor_qtimgren$ui_profiles_$$_QCoreApplication(tstate);
        if (unlikely(tmp_expression_value_11 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[43]);
        }

        if (tmp_expression_value_11 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_7);

            exception_lineno = 81;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_8 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_11, mod_consts[44]);
        if (tmp_called_value_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_7);

            exception_lineno = 81;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame.f_lineno = 81;
        tmp_args_element_value_4 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_8, mod_consts[50]);

        Py_DECREF(tmp_called_value_8);
        if (tmp_args_element_value_4 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_7);

            exception_lineno = 81;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame.f_lineno = 81;
        tmp_call_result_4 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_7, tmp_args_element_value_4);
        Py_DECREF(tmp_called_value_7);
        Py_DECREF(tmp_args_element_value_4);
        if (tmp_call_result_4 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 81;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_4);
    }
    {
        PyObject *tmp_called_value_9;
        PyObject *tmp_expression_value_12;
        PyObject *tmp_expression_value_13;
        PyObject *tmp_call_result_5;
        PyObject *tmp_args_element_value_5;
        PyObject *tmp_called_value_10;
        PyObject *tmp_expression_value_14;
        CHECK_OBJECT(par_self);
        tmp_expression_value_13 = par_self;
        tmp_expression_value_12 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_13, mod_consts[27]);
        if (tmp_expression_value_12 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 83;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_9 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_12, mod_consts[48]);
        Py_DECREF(tmp_expression_value_12);
        if (tmp_called_value_9 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 83;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_expression_value_14 = module_var_accessor_qtimgren$ui_profiles_$$_QCoreApplication(tstate);
        if (unlikely(tmp_expression_value_14 == NULL)) {
            RAISE_CURRENT_EXCEPTION_NAME_ERROR(tstate, &exception_state, mod_consts[43]);
        }

        if (tmp_expression_value_14 == NULL) {
            assert(HAS_EXCEPTION_STATE(&exception_state));

            Py_DECREF(tmp_called_value_9);

            exception_lineno = 83;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        tmp_called_value_10 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_14, mod_consts[44]);
        if (tmp_called_value_10 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_9);

            exception_lineno = 83;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame.f_lineno = 83;
        tmp_args_element_value_5 = CALL_FUNCTION_WITH_POS_ARGS3(tstate, tmp_called_value_10, mod_consts[51]);

        Py_DECREF(tmp_called_value_10);
        if (tmp_args_element_value_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);
            Py_DECREF(tmp_called_value_9);

            exception_lineno = 83;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame.f_lineno = 83;
        tmp_call_result_5 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, tmp_called_value_9, tmp_args_element_value_5);
        Py_DECREF(tmp_called_value_9);
        Py_DECREF(tmp_args_element_value_5);
        if (tmp_call_result_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 83;
            type_description_1 = "oo";
            goto frame_exception_exit_1;
        }
        Py_DECREF(tmp_call_result_5);
    }


    // Put the previous frame back on top.
    popFrameStack(tstate);

    goto frame_no_exception_1;
    frame_exception_exit_1:


    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_4a788d4b1316fa0c0d7ebed1b52367c4, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        } else if (exception_tb->tb_frame != &frame_4a788d4b1316fa0c0d7ebed1b52367c4->m_frame) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_4a788d4b1316fa0c0d7ebed1b52367c4, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        }
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_4a788d4b1316fa0c0d7ebed1b52367c4,
        type_description_1,
        par_self,
        par_profiles
    );


    // Release cached frame if used for exception.
    if (frame_4a788d4b1316fa0c0d7ebed1b52367c4 == cache_frame_4a788d4b1316fa0c0d7ebed1b52367c4) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_4a788d4b1316fa0c0d7ebed1b52367c4);
        cache_frame_4a788d4b1316fa0c0d7ebed1b52367c4 = NULL;
    }

    assertFrameObject(frame_4a788d4b1316fa0c0d7ebed1b52367c4);

    // Put the previous frame back on top.
    popFrameStack(tstate);

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;
    tmp_return_value = Py_None;
    Py_INCREF(tmp_return_value);
    goto function_return_exit;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_profiles);
    Py_DECREF(par_profiles);
    CHECK_EXCEPTION_STATE(&exception_state);
    RESTORE_ERROR_OCCURRED_STATE(tstate, &exception_state);

    return NULL;

function_return_exit:
   // Function cleanup code if any.
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_profiles);
    Py_DECREF(par_profiles);

   // Actual function exit with return value, making sure we did not make
   // the error status worse despite non-NULL return.
   CHECK_OBJECT(tmp_return_value);
   assert(had_error || !HAS_ERROR_OCCURRED(tstate));
   return tmp_return_value;
}



static PyObject *MAKE_FUNCTION_qtimgren$ui_profiles$$$function__1_setupUi() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_qtimgren$ui_profiles$$$function__1_setupUi,
        mod_consts[105],
#if PYTHON_VERSION >= 0x300
        mod_consts[106],
#endif
        code_objects_16b17377e50f407262c01bd6e73a0afa,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_qtimgren$ui_profiles,
        NULL,
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_qtimgren$ui_profiles$$$function__2_retranslateUi() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_qtimgren$ui_profiles$$$function__2_retranslateUi,
        mod_consts[36],
#if PYTHON_VERSION >= 0x300
        mod_consts[107],
#endif
        code_objects_4a788d4b1316fa0c0d7ebed1b52367c4,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_qtimgren$ui_profiles,
        NULL,
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

static function_impl_code const function_table_qtimgren$ui_profiles[] = {
    impl_qtimgren$ui_profiles$$$function__1_setupUi,
    impl_qtimgren$ui_profiles$$$function__2_retranslateUi,
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

    int offset = Nuitka_Function_GetFunctionCodeIndex(function, function_table_qtimgren$ui_profiles);

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
        module_qtimgren$ui_profiles,
        function_qualname,
        function_index,
        code_object_desc,
        constant_return_value,
        defaults,
        kw_defaults,
        doc,
        closure,
        function_table_qtimgren$ui_profiles,
        sizeof(function_table_qtimgren$ui_profiles) / sizeof(function_impl_code)
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
static char const *module_full_name = "qtimgren.ui_profiles";
#endif

// Internal entry point for module code.
PyObject *modulecode_qtimgren$ui_profiles(PyThreadState *tstate, PyObject *module, struct Nuitka_MetaPathBasedLoaderEntry const *loader_entry) {
    // Report entry to PGO.
    PGO_onModuleEntered("qtimgren$ui_profiles");

    // Store the module for future use.
    module_qtimgren$ui_profiles = module;

    moduledict_qtimgren$ui_profiles = MODULE_DICT(module_qtimgren$ui_profiles);

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
        PRINT_STRING("qtimgren$ui_profiles: Calling setupMetaPathBasedLoader().\n");
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
        NUITKA_PRINT_TRACE("qtimgren$ui_profiles: Calling createModuleConstants().\n");
        createModuleConstants(tstate);

        createModuleCodeObjects();

        init_done = true;
    }

#if defined(_NUITKA_MODULE) && 0
    PyObject *pre_load = IMPORT_EMBEDDED_MODULE(tstate, "qtimgren.ui_profiles" "-preLoad");
    if (pre_load == NULL) {
        return NULL;
    }
#endif

    // PRINT_STRING("in initqtimgren$ui_profiles\n");

#ifdef _NUITKA_PLUGIN_DILL_ENABLED
    {
        char const *module_name_c;
        if (loader_entry != NULL) {
            module_name_c = loader_entry->name;
        } else {
            PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)const_str_plain___name__);
            module_name_c = Nuitka_String_AsString(module_name);
        }

        registerDillPluginTables(tstate, module_name_c, &_method_def_reduce_compiled_function, &_method_def_create_compiled_function);
    }
#endif

    // Set "__compiled__" to what version information we have.
    UPDATE_STRING_DICT0(
        moduledict_qtimgren$ui_profiles,
        (Nuitka_StringObject *)const_str_plain___compiled__,
        Nuitka_dunder_compiled_value
    );

    // Update "__package__" value to what it ought to be.
    {
#if 0
        UPDATE_STRING_DICT0(
            moduledict_qtimgren$ui_profiles,
            (Nuitka_StringObject *)const_str_plain___package__,
            mod_consts[113]
        );
#elif 0
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)const_str_plain___name__);

        UPDATE_STRING_DICT0(
            moduledict_qtimgren$ui_profiles,
            (Nuitka_StringObject *)const_str_plain___package__,
            module_name
        );
#else

#if PYTHON_VERSION < 0x300
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)const_str_plain___name__);
        char const *module_name_cstr = PyString_AS_STRING(module_name);

        char const *last_dot = strrchr(module_name_cstr, '.');

        if (last_dot != NULL) {
            UPDATE_STRING_DICT1(
                moduledict_qtimgren$ui_profiles,
                (Nuitka_StringObject *)const_str_plain___package__,
                PyString_FromStringAndSize(module_name_cstr, last_dot - module_name_cstr)
            );
        }
#else
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)const_str_plain___name__);
        Py_ssize_t dot_index = PyUnicode_Find(module_name, const_str_dot, 0, PyUnicode_GetLength(module_name), -1);

        if (dot_index != -1) {
            UPDATE_STRING_DICT1(
                moduledict_qtimgren$ui_profiles,
                (Nuitka_StringObject *)const_str_plain___package__,
                PyUnicode_Substring(module_name, 0, dot_index)
            );
        }
#endif
#endif
    }

    CHECK_OBJECT(module_qtimgren$ui_profiles);

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    if (GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)const_str_plain___builtins__) == NULL) {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then but the module itself.
#if defined(_NUITKA_MODULE) || !0
        value = PyModule_GetDict(value);
#endif

        UPDATE_STRING_DICT0(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)const_str_plain___builtins__, value);
    }

    UPDATE_STRING_DICT0(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)const_str_plain___loader__, Nuitka_Loader_New(loader_entry));

#if PYTHON_VERSION >= 0x300
// Set the "__spec__" value

#if 0
    // Main modules just get "None" as spec.
    UPDATE_STRING_DICT0(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)const_str_plain___spec__, Py_None);
#else
    // Other modules get a "ModuleSpec" from the standard mechanism.
    {
        PyObject *bootstrap_module = getImportLibBootstrapModule();
        CHECK_OBJECT(bootstrap_module);

        PyObject *_spec_from_module = PyObject_GetAttrString(bootstrap_module, "_spec_from_module");
        CHECK_OBJECT(_spec_from_module);

        PyObject *spec_value = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, _spec_from_module, module_qtimgren$ui_profiles);
        Py_DECREF(_spec_from_module);

        // We can assume this to never fail, or else we are in trouble anyway.
        // CHECK_OBJECT(spec_value);

        if (spec_value == NULL) {
            PyErr_PrintEx(0);
            abort();
        }

// Mark the execution in the "__spec__" value.
        SET_ATTRIBUTE(tstate, spec_value, const_str_plain__initializing, Py_True);

        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)const_str_plain___spec__, spec_value);
    }
#endif
#endif

    // Temp variables if any
    PyObject *outline_0_var___class__ = NULL;
    PyObject *tmp_class_creation_1__bases = NULL;
    PyObject *tmp_class_creation_1__class_decl_dict = NULL;
    PyObject *tmp_class_creation_1__metaclass = NULL;
    PyObject *tmp_class_creation_1__prepared = NULL;
    PyObject *tmp_import_from_1__module = NULL;
    PyObject *tmp_import_from_2__module = NULL;
    PyObject *tmp_import_from_3__module = NULL;
    struct Nuitka_FrameObject *frame_5292643c84c58ca7ae9bb7bed7e3ceed;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    bool tmp_result;
    struct Nuitka_ExceptionPreservationItem exception_state = Empty_Nuitka_ExceptionPreservationItem;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_2;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_2;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_3;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_3;
    int tmp_res;
    PyObject *locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22 = NULL;
    PyObject *tmp_dictset_value;
    struct Nuitka_FrameObject *frame_a87da0f363d9e00c30155fc19acc845d_2;
    NUITKA_MAY_BE_UNUSED char const *type_description_2 = NULL;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_4;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_4;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_5;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_5;
    struct Nuitka_ExceptionPreservationItem exception_keeper_name_6;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_6;

    // Module init code if any


    // Module code.
    {
        PyObject *tmp_assign_source_1;
        tmp_assign_source_1 = Py_None;
        UPDATE_STRING_DICT0(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[52], tmp_assign_source_1);
    }
    {
        PyObject *tmp_assign_source_2;
        tmp_assign_source_2 = module_filename_obj;
        UPDATE_STRING_DICT0(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[53], tmp_assign_source_2);
    }
    frame_5292643c84c58ca7ae9bb7bed7e3ceed = MAKE_MODULE_FRAME(code_objects_5292643c84c58ca7ae9bb7bed7e3ceed, module_qtimgren$ui_profiles);

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(tstate, frame_5292643c84c58ca7ae9bb7bed7e3ceed);
    assert(Py_REFCNT(frame_5292643c84c58ca7ae9bb7bed7e3ceed) == 2);

    // Framed code:
    {
        PyObject *tmp_assattr_value_1;
        PyObject *tmp_assattr_target_1;
        tmp_assattr_value_1 = module_filename_obj;
        tmp_assattr_target_1 = module_var_accessor_qtimgren$ui_profiles_$$___spec__(tstate);
        assert(!(tmp_assattr_target_1 == NULL));
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_1, mod_consts[54], tmp_assattr_value_1);
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
        tmp_assattr_target_2 = module_var_accessor_qtimgren$ui_profiles_$$___spec__(tstate);
        assert(!(tmp_assattr_target_2 == NULL));
        tmp_result = SET_ATTRIBUTE(tstate, tmp_assattr_target_2, mod_consts[55], tmp_assattr_value_2);
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
        UPDATE_STRING_DICT0(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[56], tmp_assign_source_3);
    }
    {
        PyObject *tmp_assign_source_4;
        PyObject *tmp_name_value_1;
        PyObject *tmp_globals_arg_value_1;
        PyObject *tmp_locals_arg_value_1;
        PyObject *tmp_fromlist_value_1;
        PyObject *tmp_level_value_1;
        tmp_name_value_1 = mod_consts[57];
        tmp_globals_arg_value_1 = (PyObject *)moduledict_qtimgren$ui_profiles;
        tmp_locals_arg_value_1 = Py_None;
        tmp_fromlist_value_1 = mod_consts[58];
        tmp_level_value_1 = const_int_0;
        frame_5292643c84c58ca7ae9bb7bed7e3ceed->m_frame.f_lineno = 11;
        tmp_assign_source_4 = IMPORT_MODULE5(tstate, tmp_name_value_1, tmp_globals_arg_value_1, tmp_locals_arg_value_1, tmp_fromlist_value_1, tmp_level_value_1);
        if (tmp_assign_source_4 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto frame_exception_exit_1;
        }
        assert(tmp_import_from_1__module == NULL);
        tmp_import_from_1__module = tmp_assign_source_4;
    }
    // Tried code:
    {
        PyObject *tmp_assign_source_5;
        PyObject *tmp_import_name_from_1;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_1 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_1)) {
            tmp_assign_source_5 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_1,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[43],
                const_int_0
            );
        } else {
            tmp_assign_source_5 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_1, mod_consts[43]);
        }

        if (tmp_assign_source_5 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[43], tmp_assign_source_5);
    }
    {
        PyObject *tmp_assign_source_6;
        PyObject *tmp_import_name_from_2;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_2 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_2)) {
            tmp_assign_source_6 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_2,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[59],
                const_int_0
            );
        } else {
            tmp_assign_source_6 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_2, mod_consts[59]);
        }

        if (tmp_assign_source_6 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[59], tmp_assign_source_6);
    }
    {
        PyObject *tmp_assign_source_7;
        PyObject *tmp_import_name_from_3;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_3 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_3)) {
            tmp_assign_source_7 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_3,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[60],
                const_int_0
            );
        } else {
            tmp_assign_source_7 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_3, mod_consts[60]);
        }

        if (tmp_assign_source_7 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[60], tmp_assign_source_7);
    }
    {
        PyObject *tmp_assign_source_8;
        PyObject *tmp_import_name_from_4;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_4 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_4)) {
            tmp_assign_source_8 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_4,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[61],
                const_int_0
            );
        } else {
            tmp_assign_source_8 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_4, mod_consts[61]);
        }

        if (tmp_assign_source_8 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[61], tmp_assign_source_8);
    }
    {
        PyObject *tmp_assign_source_9;
        PyObject *tmp_import_name_from_5;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_5 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_5)) {
            tmp_assign_source_9 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_5,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[40],
                const_int_0
            );
        } else {
            tmp_assign_source_9 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_5, mod_consts[40]);
        }

        if (tmp_assign_source_9 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[40], tmp_assign_source_9);
    }
    {
        PyObject *tmp_assign_source_10;
        PyObject *tmp_import_name_from_6;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_6 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_6)) {
            tmp_assign_source_10 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_6,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[62],
                const_int_0
            );
        } else {
            tmp_assign_source_10 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_6, mod_consts[62]);
        }

        if (tmp_assign_source_10 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[62], tmp_assign_source_10);
    }
    {
        PyObject *tmp_assign_source_11;
        PyObject *tmp_import_name_from_7;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_7 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_7)) {
            tmp_assign_source_11 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_7,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[63],
                const_int_0
            );
        } else {
            tmp_assign_source_11 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_7, mod_consts[63]);
        }

        if (tmp_assign_source_11 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[63], tmp_assign_source_11);
    }
    {
        PyObject *tmp_assign_source_12;
        PyObject *tmp_import_name_from_8;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_8 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_8)) {
            tmp_assign_source_12 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_8,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[64],
                const_int_0
            );
        } else {
            tmp_assign_source_12 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_8, mod_consts[64]);
        }

        if (tmp_assign_source_12 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[64], tmp_assign_source_12);
    }
    {
        PyObject *tmp_assign_source_13;
        PyObject *tmp_import_name_from_9;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_9 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_9)) {
            tmp_assign_source_13 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_9,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[65],
                const_int_0
            );
        } else {
            tmp_assign_source_13 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_9, mod_consts[65]);
        }

        if (tmp_assign_source_13 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[65], tmp_assign_source_13);
    }
    {
        PyObject *tmp_assign_source_14;
        PyObject *tmp_import_name_from_10;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_10 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_10)) {
            tmp_assign_source_14 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_10,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[66],
                const_int_0
            );
        } else {
            tmp_assign_source_14 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_10, mod_consts[66]);
        }

        if (tmp_assign_source_14 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[66], tmp_assign_source_14);
    }
    {
        PyObject *tmp_assign_source_15;
        PyObject *tmp_import_name_from_11;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_11 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_11)) {
            tmp_assign_source_15 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_11,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[67],
                const_int_0
            );
        } else {
            tmp_assign_source_15 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_11, mod_consts[67]);
        }

        if (tmp_assign_source_15 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[67], tmp_assign_source_15);
    }
    {
        PyObject *tmp_assign_source_16;
        PyObject *tmp_import_name_from_12;
        CHECK_OBJECT(tmp_import_from_1__module);
        tmp_import_name_from_12 = tmp_import_from_1__module;
        if (PyModule_Check(tmp_import_name_from_12)) {
            tmp_assign_source_16 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_12,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[68],
                const_int_0
            );
        } else {
            tmp_assign_source_16 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_12, mod_consts[68]);
        }

        if (tmp_assign_source_16 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 11;

            goto try_except_handler_1;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[68], tmp_assign_source_16);
    }
    goto try_end_1;
    // Exception handler code:
    try_except_handler_1:;
    exception_keeper_lineno_1 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_1 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    CHECK_OBJECT(tmp_import_from_1__module);
    Py_DECREF(tmp_import_from_1__module);
    tmp_import_from_1__module = NULL;
    // Re-raise.
    exception_state = exception_keeper_name_1;
    exception_lineno = exception_keeper_lineno_1;

    goto frame_exception_exit_1;
    // End of try:
    try_end_1:;
    CHECK_OBJECT(tmp_import_from_1__module);
    Py_DECREF(tmp_import_from_1__module);
    tmp_import_from_1__module = NULL;
    {
        PyObject *tmp_assign_source_17;
        PyObject *tmp_name_value_2;
        PyObject *tmp_globals_arg_value_2;
        PyObject *tmp_locals_arg_value_2;
        PyObject *tmp_fromlist_value_2;
        PyObject *tmp_level_value_2;
        tmp_name_value_2 = mod_consts[69];
        tmp_globals_arg_value_2 = (PyObject *)moduledict_qtimgren$ui_profiles;
        tmp_locals_arg_value_2 = Py_None;
        tmp_fromlist_value_2 = mod_consts[70];
        tmp_level_value_2 = const_int_0;
        frame_5292643c84c58ca7ae9bb7bed7e3ceed->m_frame.f_lineno = 14;
        tmp_assign_source_17 = IMPORT_MODULE5(tstate, tmp_name_value_2, tmp_globals_arg_value_2, tmp_locals_arg_value_2, tmp_fromlist_value_2, tmp_level_value_2);
        if (tmp_assign_source_17 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto frame_exception_exit_1;
        }
        assert(tmp_import_from_2__module == NULL);
        tmp_import_from_2__module = tmp_assign_source_17;
    }
    // Tried code:
    {
        PyObject *tmp_assign_source_18;
        PyObject *tmp_import_name_from_13;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_13 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_13)) {
            tmp_assign_source_18 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_13,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[71],
                const_int_0
            );
        } else {
            tmp_assign_source_18 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_13, mod_consts[71]);
        }

        if (tmp_assign_source_18 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[71], tmp_assign_source_18);
    }
    {
        PyObject *tmp_assign_source_19;
        PyObject *tmp_import_name_from_14;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_14 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_14)) {
            tmp_assign_source_19 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_14,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[72],
                const_int_0
            );
        } else {
            tmp_assign_source_19 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_14, mod_consts[72]);
        }

        if (tmp_assign_source_19 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[72], tmp_assign_source_19);
    }
    {
        PyObject *tmp_assign_source_20;
        PyObject *tmp_import_name_from_15;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_15 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_15)) {
            tmp_assign_source_20 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_15,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[73],
                const_int_0
            );
        } else {
            tmp_assign_source_20 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_15, mod_consts[73]);
        }

        if (tmp_assign_source_20 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[73], tmp_assign_source_20);
    }
    {
        PyObject *tmp_assign_source_21;
        PyObject *tmp_import_name_from_16;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_16 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_16)) {
            tmp_assign_source_21 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_16,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[74],
                const_int_0
            );
        } else {
            tmp_assign_source_21 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_16, mod_consts[74]);
        }

        if (tmp_assign_source_21 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[74], tmp_assign_source_21);
    }
    {
        PyObject *tmp_assign_source_22;
        PyObject *tmp_import_name_from_17;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_17 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_17)) {
            tmp_assign_source_22 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_17,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[75],
                const_int_0
            );
        } else {
            tmp_assign_source_22 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_17, mod_consts[75]);
        }

        if (tmp_assign_source_22 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[75], tmp_assign_source_22);
    }
    {
        PyObject *tmp_assign_source_23;
        PyObject *tmp_import_name_from_18;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_18 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_18)) {
            tmp_assign_source_23 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_18,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[76],
                const_int_0
            );
        } else {
            tmp_assign_source_23 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_18, mod_consts[76]);
        }

        if (tmp_assign_source_23 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[76], tmp_assign_source_23);
    }
    {
        PyObject *tmp_assign_source_24;
        PyObject *tmp_import_name_from_19;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_19 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_19)) {
            tmp_assign_source_24 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_19,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[77],
                const_int_0
            );
        } else {
            tmp_assign_source_24 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_19, mod_consts[77]);
        }

        if (tmp_assign_source_24 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[77], tmp_assign_source_24);
    }
    {
        PyObject *tmp_assign_source_25;
        PyObject *tmp_import_name_from_20;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_20 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_20)) {
            tmp_assign_source_25 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_20,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[78],
                const_int_0
            );
        } else {
            tmp_assign_source_25 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_20, mod_consts[78]);
        }

        if (tmp_assign_source_25 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[78], tmp_assign_source_25);
    }
    {
        PyObject *tmp_assign_source_26;
        PyObject *tmp_import_name_from_21;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_21 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_21)) {
            tmp_assign_source_26 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_21,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[79],
                const_int_0
            );
        } else {
            tmp_assign_source_26 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_21, mod_consts[79]);
        }

        if (tmp_assign_source_26 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[79], tmp_assign_source_26);
    }
    {
        PyObject *tmp_assign_source_27;
        PyObject *tmp_import_name_from_22;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_22 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_22)) {
            tmp_assign_source_27 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_22,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[80],
                const_int_0
            );
        } else {
            tmp_assign_source_27 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_22, mod_consts[80]);
        }

        if (tmp_assign_source_27 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[80], tmp_assign_source_27);
    }
    {
        PyObject *tmp_assign_source_28;
        PyObject *tmp_import_name_from_23;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_23 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_23)) {
            tmp_assign_source_28 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_23,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[81],
                const_int_0
            );
        } else {
            tmp_assign_source_28 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_23, mod_consts[81]);
        }

        if (tmp_assign_source_28 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[81], tmp_assign_source_28);
    }
    {
        PyObject *tmp_assign_source_29;
        PyObject *tmp_import_name_from_24;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_24 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_24)) {
            tmp_assign_source_29 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_24,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[82],
                const_int_0
            );
        } else {
            tmp_assign_source_29 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_24, mod_consts[82]);
        }

        if (tmp_assign_source_29 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[82], tmp_assign_source_29);
    }
    {
        PyObject *tmp_assign_source_30;
        PyObject *tmp_import_name_from_25;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_25 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_25)) {
            tmp_assign_source_30 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_25,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[83],
                const_int_0
            );
        } else {
            tmp_assign_source_30 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_25, mod_consts[83]);
        }

        if (tmp_assign_source_30 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[83], tmp_assign_source_30);
    }
    {
        PyObject *tmp_assign_source_31;
        PyObject *tmp_import_name_from_26;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_26 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_26)) {
            tmp_assign_source_31 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_26,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[84],
                const_int_0
            );
        } else {
            tmp_assign_source_31 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_26, mod_consts[84]);
        }

        if (tmp_assign_source_31 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[84], tmp_assign_source_31);
    }
    {
        PyObject *tmp_assign_source_32;
        PyObject *tmp_import_name_from_27;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_27 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_27)) {
            tmp_assign_source_32 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_27,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[85],
                const_int_0
            );
        } else {
            tmp_assign_source_32 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_27, mod_consts[85]);
        }

        if (tmp_assign_source_32 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[85], tmp_assign_source_32);
    }
    {
        PyObject *tmp_assign_source_33;
        PyObject *tmp_import_name_from_28;
        CHECK_OBJECT(tmp_import_from_2__module);
        tmp_import_name_from_28 = tmp_import_from_2__module;
        if (PyModule_Check(tmp_import_name_from_28)) {
            tmp_assign_source_33 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_28,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[86],
                const_int_0
            );
        } else {
            tmp_assign_source_33 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_28, mod_consts[86]);
        }

        if (tmp_assign_source_33 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 14;

            goto try_except_handler_2;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[86], tmp_assign_source_33);
    }
    goto try_end_2;
    // Exception handler code:
    try_except_handler_2:;
    exception_keeper_lineno_2 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_2 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    CHECK_OBJECT(tmp_import_from_2__module);
    Py_DECREF(tmp_import_from_2__module);
    tmp_import_from_2__module = NULL;
    // Re-raise.
    exception_state = exception_keeper_name_2;
    exception_lineno = exception_keeper_lineno_2;

    goto frame_exception_exit_1;
    // End of try:
    try_end_2:;
    CHECK_OBJECT(tmp_import_from_2__module);
    Py_DECREF(tmp_import_from_2__module);
    tmp_import_from_2__module = NULL;
    {
        PyObject *tmp_assign_source_34;
        PyObject *tmp_name_value_3;
        PyObject *tmp_globals_arg_value_3;
        PyObject *tmp_locals_arg_value_3;
        PyObject *tmp_fromlist_value_3;
        PyObject *tmp_level_value_3;
        tmp_name_value_3 = mod_consts[87];
        tmp_globals_arg_value_3 = (PyObject *)moduledict_qtimgren$ui_profiles;
        tmp_locals_arg_value_3 = Py_None;
        tmp_fromlist_value_3 = mod_consts[88];
        tmp_level_value_3 = const_int_0;
        frame_5292643c84c58ca7ae9bb7bed7e3ceed->m_frame.f_lineno = 18;
        tmp_assign_source_34 = IMPORT_MODULE5(tstate, tmp_name_value_3, tmp_globals_arg_value_3, tmp_locals_arg_value_3, tmp_fromlist_value_3, tmp_level_value_3);
        if (tmp_assign_source_34 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto frame_exception_exit_1;
        }
        assert(tmp_import_from_3__module == NULL);
        tmp_import_from_3__module = tmp_assign_source_34;
    }
    // Tried code:
    {
        PyObject *tmp_assign_source_35;
        PyObject *tmp_import_name_from_29;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_29 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_29)) {
            tmp_assign_source_35 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_29,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[89],
                const_int_0
            );
        } else {
            tmp_assign_source_35 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_29, mod_consts[89]);
        }

        if (tmp_assign_source_35 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[89], tmp_assign_source_35);
    }
    {
        PyObject *tmp_assign_source_36;
        PyObject *tmp_import_name_from_30;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_30 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_30)) {
            tmp_assign_source_36 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_30,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[19],
                const_int_0
            );
        } else {
            tmp_assign_source_36 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_30, mod_consts[19]);
        }

        if (tmp_assign_source_36 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[19], tmp_assign_source_36);
    }
    {
        PyObject *tmp_assign_source_37;
        PyObject *tmp_import_name_from_31;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_31 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_31)) {
            tmp_assign_source_37 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_31,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[90],
                const_int_0
            );
        } else {
            tmp_assign_source_37 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_31, mod_consts[90]);
        }

        if (tmp_assign_source_37 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[90], tmp_assign_source_37);
    }
    {
        PyObject *tmp_assign_source_38;
        PyObject *tmp_import_name_from_32;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_32 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_32)) {
            tmp_assign_source_38 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_32,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[91],
                const_int_0
            );
        } else {
            tmp_assign_source_38 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_32, mod_consts[91]);
        }

        if (tmp_assign_source_38 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[91], tmp_assign_source_38);
    }
    {
        PyObject *tmp_assign_source_39;
        PyObject *tmp_import_name_from_33;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_33 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_33)) {
            tmp_assign_source_39 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_33,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[30],
                const_int_0
            );
        } else {
            tmp_assign_source_39 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_33, mod_consts[30]);
        }

        if (tmp_assign_source_39 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[30], tmp_assign_source_39);
    }
    {
        PyObject *tmp_assign_source_40;
        PyObject *tmp_import_name_from_34;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_34 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_34)) {
            tmp_assign_source_40 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_34,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[7],
                const_int_0
            );
        } else {
            tmp_assign_source_40 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_34, mod_consts[7]);
        }

        if (tmp_assign_source_40 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[7], tmp_assign_source_40);
    }
    {
        PyObject *tmp_assign_source_41;
        PyObject *tmp_import_name_from_35;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_35 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_35)) {
            tmp_assign_source_41 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_35,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[92],
                const_int_0
            );
        } else {
            tmp_assign_source_41 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_35, mod_consts[92]);
        }

        if (tmp_assign_source_41 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[92], tmp_assign_source_41);
    }
    {
        PyObject *tmp_assign_source_42;
        PyObject *tmp_import_name_from_36;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_36 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_36)) {
            tmp_assign_source_42 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_36,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[24],
                const_int_0
            );
        } else {
            tmp_assign_source_42 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_36, mod_consts[24]);
        }

        if (tmp_assign_source_42 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[24], tmp_assign_source_42);
    }
    {
        PyObject *tmp_assign_source_43;
        PyObject *tmp_import_name_from_37;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_37 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_37)) {
            tmp_assign_source_43 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_37,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[93],
                const_int_0
            );
        } else {
            tmp_assign_source_43 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_37, mod_consts[93]);
        }

        if (tmp_assign_source_43 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[93], tmp_assign_source_43);
    }
    {
        PyObject *tmp_assign_source_44;
        PyObject *tmp_import_name_from_38;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_38 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_38)) {
            tmp_assign_source_44 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_38,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[15],
                const_int_0
            );
        } else {
            tmp_assign_source_44 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_38, mod_consts[15]);
        }

        if (tmp_assign_source_44 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[15], tmp_assign_source_44);
    }
    {
        PyObject *tmp_assign_source_45;
        PyObject *tmp_import_name_from_39;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_39 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_39)) {
            tmp_assign_source_45 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_39,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[10],
                const_int_0
            );
        } else {
            tmp_assign_source_45 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_39, mod_consts[10]);
        }

        if (tmp_assign_source_45 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[10], tmp_assign_source_45);
    }
    {
        PyObject *tmp_assign_source_46;
        PyObject *tmp_import_name_from_40;
        CHECK_OBJECT(tmp_import_from_3__module);
        tmp_import_name_from_40 = tmp_import_from_3__module;
        if (PyModule_Check(tmp_import_name_from_40)) {
            tmp_assign_source_46 = IMPORT_NAME_OR_MODULE(
                tstate,
                tmp_import_name_from_40,
                (PyObject *)moduledict_qtimgren$ui_profiles,
                mod_consts[94],
                const_int_0
            );
        } else {
            tmp_assign_source_46 = IMPORT_NAME_FROM_MODULE(tstate, tmp_import_name_from_40, mod_consts[94]);
        }

        if (tmp_assign_source_46 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 18;

            goto try_except_handler_3;
        }
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[94], tmp_assign_source_46);
    }
    goto try_end_3;
    // Exception handler code:
    try_except_handler_3:;
    exception_keeper_lineno_3 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_3 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    CHECK_OBJECT(tmp_import_from_3__module);
    Py_DECREF(tmp_import_from_3__module);
    tmp_import_from_3__module = NULL;
    // Re-raise.
    exception_state = exception_keeper_name_3;
    exception_lineno = exception_keeper_lineno_3;

    goto frame_exception_exit_1;
    // End of try:
    try_end_3:;
    CHECK_OBJECT(tmp_import_from_3__module);
    Py_DECREF(tmp_import_from_3__module);
    tmp_import_from_3__module = NULL;
    // Tried code:
    {
        PyObject *tmp_assign_source_47;
        PyObject *tmp_dircall_arg1_1;
        tmp_dircall_arg1_1 = mod_consts[95];
        Py_INCREF(tmp_dircall_arg1_1);

        {
            PyObject *dir_call_args[] = {tmp_dircall_arg1_1};
            tmp_assign_source_47 = impl_qtimgren$__main__$$$helper_function__mro_entries_conversion(tstate, dir_call_args);
        }
        if (tmp_assign_source_47 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        assert(tmp_class_creation_1__bases == NULL);
        tmp_class_creation_1__bases = tmp_assign_source_47;
    }
    {
        PyObject *tmp_assign_source_48;
        tmp_assign_source_48 = MAKE_DICT_EMPTY(tstate);
        assert(tmp_class_creation_1__class_decl_dict == NULL);
        tmp_class_creation_1__class_decl_dict = tmp_assign_source_48;
    }
    {
        PyObject *tmp_assign_source_49;
        PyObject *tmp_metaclass_value_1;
        nuitka_bool tmp_condition_result_1;
        int tmp_truth_name_1;
        PyObject *tmp_type_arg_1;
        PyObject *tmp_expression_value_1;
        PyObject *tmp_subscript_value_1;
        PyObject *tmp_bases_value_1;
        CHECK_OBJECT(tmp_class_creation_1__bases);
        tmp_truth_name_1 = CHECK_IF_TRUE(tmp_class_creation_1__bases);
        if (tmp_truth_name_1 == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        tmp_condition_result_1 = tmp_truth_name_1 == 0 ? NUITKA_BOOL_FALSE : NUITKA_BOOL_TRUE;
        if (tmp_condition_result_1 == NUITKA_BOOL_TRUE) {
            goto condexpr_true_1;
        } else {
            goto condexpr_false_1;
        }
        condexpr_true_1:;
        CHECK_OBJECT(tmp_class_creation_1__bases);
        tmp_expression_value_1 = tmp_class_creation_1__bases;
        tmp_subscript_value_1 = const_int_0;
        tmp_type_arg_1 = LOOKUP_SUBSCRIPT_CONST(tstate, tmp_expression_value_1, tmp_subscript_value_1, 0);
        if (tmp_type_arg_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        tmp_metaclass_value_1 = BUILTIN_TYPE1(tmp_type_arg_1);
        Py_DECREF(tmp_type_arg_1);
        if (tmp_metaclass_value_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        goto condexpr_end_1;
        condexpr_false_1:;
        tmp_metaclass_value_1 = (PyObject *)&PyType_Type;
        Py_INCREF(tmp_metaclass_value_1);
        condexpr_end_1:;
        CHECK_OBJECT(tmp_class_creation_1__bases);
        tmp_bases_value_1 = tmp_class_creation_1__bases;
        tmp_assign_source_49 = SELECT_METACLASS(tstate, tmp_metaclass_value_1, tmp_bases_value_1);
        Py_DECREF(tmp_metaclass_value_1);
        if (tmp_assign_source_49 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        assert(tmp_class_creation_1__metaclass == NULL);
        tmp_class_creation_1__metaclass = tmp_assign_source_49;
    }
    {
        bool tmp_condition_result_2;
        PyObject *tmp_expression_value_2;
        CHECK_OBJECT(tmp_class_creation_1__metaclass);
        tmp_expression_value_2 = tmp_class_creation_1__metaclass;
        tmp_res = HAS_ATTR_BOOL2(tstate, tmp_expression_value_2, mod_consts[96]);
        if (tmp_res == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        tmp_condition_result_2 = (tmp_res != 0) ? true : false;
        if (tmp_condition_result_2 != false) {
            goto branch_yes_1;
        } else {
            goto branch_no_1;
        }
    }
    branch_yes_1:;
    {
        PyObject *tmp_assign_source_50;
        PyObject *tmp_called_value_1;
        PyObject *tmp_expression_value_3;
        PyObject *tmp_args_value_1;
        PyObject *tmp_tuple_element_1;
        PyObject *tmp_kwargs_value_1;
        CHECK_OBJECT(tmp_class_creation_1__metaclass);
        tmp_expression_value_3 = tmp_class_creation_1__metaclass;
        tmp_called_value_1 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_3, mod_consts[96]);
        if (tmp_called_value_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        tmp_tuple_element_1 = mod_consts[97];
        tmp_args_value_1 = MAKE_TUPLE_EMPTY(tstate, 2);
        PyTuple_SET_ITEM0(tmp_args_value_1, 0, tmp_tuple_element_1);
        CHECK_OBJECT(tmp_class_creation_1__bases);
        tmp_tuple_element_1 = tmp_class_creation_1__bases;
        PyTuple_SET_ITEM0(tmp_args_value_1, 1, tmp_tuple_element_1);
        CHECK_OBJECT(tmp_class_creation_1__class_decl_dict);
        tmp_kwargs_value_1 = tmp_class_creation_1__class_decl_dict;
        frame_5292643c84c58ca7ae9bb7bed7e3ceed->m_frame.f_lineno = 22;
        tmp_assign_source_50 = CALL_FUNCTION(tstate, tmp_called_value_1, tmp_args_value_1, tmp_kwargs_value_1);
        Py_DECREF(tmp_called_value_1);
        Py_DECREF(tmp_args_value_1);
        if (tmp_assign_source_50 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        assert(tmp_class_creation_1__prepared == NULL);
        tmp_class_creation_1__prepared = tmp_assign_source_50;
    }
    {
        bool tmp_condition_result_3;
        PyObject *tmp_operand_value_1;
        PyObject *tmp_expression_value_4;
        CHECK_OBJECT(tmp_class_creation_1__prepared);
        tmp_expression_value_4 = tmp_class_creation_1__prepared;
        tmp_res = HAS_ATTR_BOOL2(tstate, tmp_expression_value_4, mod_consts[98]);
        if (tmp_res == -1) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        tmp_operand_value_1 = (tmp_res != 0) ? Py_True : Py_False;
        tmp_res = CHECK_IF_TRUE(tmp_operand_value_1);
        assert(!(tmp_res == -1));
        tmp_condition_result_3 = (tmp_res == 0) ? true : false;
        if (tmp_condition_result_3 != false) {
            goto branch_yes_2;
        } else {
            goto branch_no_2;
        }
    }
    branch_yes_2:;
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        PyObject *tmp_mod_expr_left_1;
        PyObject *tmp_mod_expr_right_1;
        PyObject *tmp_tuple_element_2;
        PyObject *tmp_expression_value_5;
        PyObject *tmp_name_value_4;
        PyObject *tmp_default_value_1;
        tmp_mod_expr_left_1 = mod_consts[99];
        CHECK_OBJECT(tmp_class_creation_1__metaclass);
        tmp_expression_value_5 = tmp_class_creation_1__metaclass;
        tmp_name_value_4 = mod_consts[100];
        tmp_default_value_1 = mod_consts[101];
        tmp_tuple_element_2 = BUILTIN_GETATTR(tstate, tmp_expression_value_5, tmp_name_value_4, tmp_default_value_1);
        if (tmp_tuple_element_2 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        tmp_mod_expr_right_1 = MAKE_TUPLE_EMPTY(tstate, 2);
        {
            PyObject *tmp_expression_value_6;
            PyObject *tmp_type_arg_2;
            PyTuple_SET_ITEM(tmp_mod_expr_right_1, 0, tmp_tuple_element_2);
            CHECK_OBJECT(tmp_class_creation_1__prepared);
            tmp_type_arg_2 = tmp_class_creation_1__prepared;
            tmp_expression_value_6 = BUILTIN_TYPE1(tmp_type_arg_2);
            assert(!(tmp_expression_value_6 == NULL));
            tmp_tuple_element_2 = LOOKUP_ATTRIBUTE(tstate, tmp_expression_value_6, mod_consts[100]);
            Py_DECREF(tmp_expression_value_6);
            if (tmp_tuple_element_2 == NULL) {
                assert(HAS_ERROR_OCCURRED(tstate));

                FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


                exception_lineno = 22;

                goto tuple_build_exception_1;
            }
            PyTuple_SET_ITEM(tmp_mod_expr_right_1, 1, tmp_tuple_element_2);
        }
        goto tuple_build_noexception_1;
        // Exception handling pass through code for tuple_build:
        tuple_build_exception_1:;
        Py_DECREF(tmp_mod_expr_right_1);
        goto try_except_handler_4;
        // Finished with no exception for tuple_build:
        tuple_build_noexception_1:;
        tmp_make_exception_arg_1 = BINARY_OPERATION_MOD_OBJECT_UNICODE_TUPLE(tmp_mod_expr_left_1, tmp_mod_expr_right_1);
        Py_DECREF(tmp_mod_expr_right_1);
        if (tmp_make_exception_arg_1 == NULL) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_4;
        }
        frame_5292643c84c58ca7ae9bb7bed7e3ceed->m_frame.f_lineno = 22;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(tstate, PyExc_TypeError, tmp_make_exception_arg_1);
        Py_DECREF(tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_state.exception_type = tmp_raise_type_1;
        exception_lineno = 22;
        RAISE_EXCEPTION_WITH_TYPE(tstate, &exception_state);

        goto try_except_handler_4;
    }
    branch_no_2:;
    goto branch_end_1;
    branch_no_1:;
    {
        PyObject *tmp_assign_source_51;
        tmp_assign_source_51 = MAKE_DICT_EMPTY(tstate);
        assert(tmp_class_creation_1__prepared == NULL);
        tmp_class_creation_1__prepared = tmp_assign_source_51;
    }
    branch_end_1:;
    {
        PyObject *tmp_assign_source_52;
        {
            PyObject *tmp_set_locals_1;
            CHECK_OBJECT(tmp_class_creation_1__prepared);
            tmp_set_locals_1 = tmp_class_creation_1__prepared;
            locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22 = tmp_set_locals_1;
            Py_INCREF(tmp_set_locals_1);
        }
        // Tried code:
        // Tried code:
        tmp_dictset_value = mod_consts[102];
        tmp_res = PyObject_SetItem(locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22, mod_consts[103], tmp_dictset_value);
        if (tmp_res != 0) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_6;
        }
        tmp_dictset_value = mod_consts[97];
        tmp_res = PyObject_SetItem(locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22, mod_consts[104], tmp_dictset_value);
        if (tmp_res != 0) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_6;
        }
        frame_a87da0f363d9e00c30155fc19acc845d_2 = MAKE_CLASS_FRAME(tstate, code_objects_a87da0f363d9e00c30155fc19acc845d, module_qtimgren$ui_profiles, NULL, sizeof(void *));

        // Push the new frame as the currently active one, and we should be exclusively
        // owning it.
        pushFrameStackCompiledFrame(tstate, frame_a87da0f363d9e00c30155fc19acc845d_2);
        assert(Py_REFCNT(frame_a87da0f363d9e00c30155fc19acc845d_2) == 2);

        // Framed code:


        tmp_dictset_value = MAKE_FUNCTION_qtimgren$ui_profiles$$$function__1_setupUi();

        tmp_res = PyObject_SetItem(locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22, mod_consts[105], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        if (tmp_res != 0) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 23;
            type_description_2 = "o";
            goto frame_exception_exit_2;
        }


        tmp_dictset_value = MAKE_FUNCTION_qtimgren$ui_profiles$$$function__2_retranslateUi();

        tmp_res = PyObject_SetItem(locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22, mod_consts[36], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        if (tmp_res != 0) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 74;
            type_description_2 = "o";
            goto frame_exception_exit_2;
        }


        // Put the previous frame back on top.
        popFrameStack(tstate);

        goto frame_no_exception_1;
        frame_exception_exit_2:


        {
            PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);
            if (exception_tb == NULL) {
                exception_tb = MAKE_TRACEBACK(frame_a87da0f363d9e00c30155fc19acc845d_2, exception_lineno);
                SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
            } else if (exception_tb->tb_frame != &frame_a87da0f363d9e00c30155fc19acc845d_2->m_frame) {
                exception_tb = ADD_TRACEBACK(exception_tb, frame_a87da0f363d9e00c30155fc19acc845d_2, exception_lineno);
                SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
            }
        }

        // Attaches locals to frame if any.
        Nuitka_Frame_AttachLocals(
            frame_a87da0f363d9e00c30155fc19acc845d_2,
            type_description_2,
            outline_0_var___class__
        );



        assertFrameObject(frame_a87da0f363d9e00c30155fc19acc845d_2);

        // Put the previous frame back on top.
        popFrameStack(tstate);

        // Return the error.
        goto nested_frame_exit_1;
        frame_no_exception_1:;
        goto skip_nested_handling_1;
        nested_frame_exit_1:;

        goto try_except_handler_6;
        skip_nested_handling_1:;
        {
            nuitka_bool tmp_condition_result_4;
            PyObject *tmp_cmp_expr_left_1;
            PyObject *tmp_cmp_expr_right_1;
            CHECK_OBJECT(tmp_class_creation_1__bases);
            tmp_cmp_expr_left_1 = tmp_class_creation_1__bases;
            tmp_cmp_expr_right_1 = mod_consts[95];
            tmp_condition_result_4 = RICH_COMPARE_NE_NBOOL_OBJECT_TUPLE(tmp_cmp_expr_left_1, tmp_cmp_expr_right_1);
            if (tmp_condition_result_4 == NUITKA_BOOL_EXCEPTION) {
                assert(HAS_ERROR_OCCURRED(tstate));

                FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


                exception_lineno = 22;

                goto try_except_handler_6;
            }
            if (tmp_condition_result_4 == NUITKA_BOOL_TRUE) {
                goto branch_yes_3;
            } else {
                goto branch_no_3;
            }
        }
        branch_yes_3:;
        tmp_dictset_value = mod_consts[95];
        tmp_res = PyObject_SetItem(locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22, mod_consts[108], tmp_dictset_value);
        if (tmp_res != 0) {
            assert(HAS_ERROR_OCCURRED(tstate));

            FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


            exception_lineno = 22;

            goto try_except_handler_6;
        }
        branch_no_3:;
        {
            PyObject *tmp_assign_source_53;
            PyObject *tmp_called_value_2;
            PyObject *tmp_args_value_2;
            PyObject *tmp_tuple_element_3;
            PyObject *tmp_kwargs_value_2;
            CHECK_OBJECT(tmp_class_creation_1__metaclass);
            tmp_called_value_2 = tmp_class_creation_1__metaclass;
            tmp_tuple_element_3 = mod_consts[97];
            tmp_args_value_2 = MAKE_TUPLE_EMPTY(tstate, 3);
            PyTuple_SET_ITEM0(tmp_args_value_2, 0, tmp_tuple_element_3);
            CHECK_OBJECT(tmp_class_creation_1__bases);
            tmp_tuple_element_3 = tmp_class_creation_1__bases;
            PyTuple_SET_ITEM0(tmp_args_value_2, 1, tmp_tuple_element_3);
            tmp_tuple_element_3 = locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22;
            PyTuple_SET_ITEM0(tmp_args_value_2, 2, tmp_tuple_element_3);
            CHECK_OBJECT(tmp_class_creation_1__class_decl_dict);
            tmp_kwargs_value_2 = tmp_class_creation_1__class_decl_dict;
            frame_5292643c84c58ca7ae9bb7bed7e3ceed->m_frame.f_lineno = 22;
            tmp_assign_source_53 = CALL_FUNCTION(tstate, tmp_called_value_2, tmp_args_value_2, tmp_kwargs_value_2);
            Py_DECREF(tmp_args_value_2);
            if (tmp_assign_source_53 == NULL) {
                assert(HAS_ERROR_OCCURRED(tstate));

                FETCH_ERROR_OCCURRED_STATE(tstate, &exception_state);


                exception_lineno = 22;

                goto try_except_handler_6;
            }
            assert(outline_0_var___class__ == NULL);
            outline_0_var___class__ = tmp_assign_source_53;
        }
        CHECK_OBJECT(outline_0_var___class__);
        tmp_assign_source_52 = outline_0_var___class__;
        Py_INCREF(tmp_assign_source_52);
        goto try_return_handler_6;
        NUITKA_CANNOT_GET_HERE("tried codes exits in all cases");
        return NULL;
        // Return handler code:
        try_return_handler_6:;
        Py_DECREF(locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22);
        locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22 = NULL;
        goto try_return_handler_5;
        // Exception handler code:
        try_except_handler_6:;
        exception_keeper_lineno_4 = exception_lineno;
        exception_lineno = 0;
        exception_keeper_name_4 = exception_state;
        INIT_ERROR_OCCURRED_STATE(&exception_state);

        Py_DECREF(locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22);
        locals_qtimgren$ui_profiles$$$class__1_Ui_profiles_22 = NULL;
        // Re-raise.
        exception_state = exception_keeper_name_4;
        exception_lineno = exception_keeper_lineno_4;

        goto try_except_handler_5;
        // End of try:
        NUITKA_CANNOT_GET_HERE("tried codes exits in all cases");
        return NULL;
        // Return handler code:
        try_return_handler_5:;
        CHECK_OBJECT(outline_0_var___class__);
        Py_DECREF(outline_0_var___class__);
        outline_0_var___class__ = NULL;
        goto outline_result_1;
        // Exception handler code:
        try_except_handler_5:;
        exception_keeper_lineno_5 = exception_lineno;
        exception_lineno = 0;
        exception_keeper_name_5 = exception_state;
        INIT_ERROR_OCCURRED_STATE(&exception_state);

        // Re-raise.
        exception_state = exception_keeper_name_5;
        exception_lineno = exception_keeper_lineno_5;

        goto outline_exception_1;
        // End of try:
        NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
        return NULL;
        outline_exception_1:;
        exception_lineno = 22;
        goto try_except_handler_4;
        outline_result_1:;
        UPDATE_STRING_DICT1(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)mod_consts[97], tmp_assign_source_52);
    }
    goto try_end_4;
    // Exception handler code:
    try_except_handler_4:;
    exception_keeper_lineno_6 = exception_lineno;
    exception_lineno = 0;
    exception_keeper_name_6 = exception_state;
    INIT_ERROR_OCCURRED_STATE(&exception_state);

    Py_XDECREF(tmp_class_creation_1__bases);
    tmp_class_creation_1__bases = NULL;
    Py_XDECREF(tmp_class_creation_1__class_decl_dict);
    tmp_class_creation_1__class_decl_dict = NULL;
    Py_XDECREF(tmp_class_creation_1__metaclass);
    tmp_class_creation_1__metaclass = NULL;
    Py_XDECREF(tmp_class_creation_1__prepared);
    tmp_class_creation_1__prepared = NULL;
    // Re-raise.
    exception_state = exception_keeper_name_6;
    exception_lineno = exception_keeper_lineno_6;

    goto frame_exception_exit_1;
    // End of try:
    try_end_4:;


    // Put the previous frame back on top.
    popFrameStack(tstate);

    goto frame_no_exception_2;
    frame_exception_exit_1:


    {
        PyTracebackObject *exception_tb = GET_EXCEPTION_STATE_TRACEBACK(&exception_state);
        if (exception_tb == NULL) {
            exception_tb = MAKE_TRACEBACK(frame_5292643c84c58ca7ae9bb7bed7e3ceed, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        } else if (exception_tb->tb_frame != &frame_5292643c84c58ca7ae9bb7bed7e3ceed->m_frame) {
            exception_tb = ADD_TRACEBACK(exception_tb, frame_5292643c84c58ca7ae9bb7bed7e3ceed, exception_lineno);
            SET_EXCEPTION_STATE_TRACEBACK(&exception_state, exception_tb);
        }
    }



    assertFrameObject(frame_5292643c84c58ca7ae9bb7bed7e3ceed);

    // Put the previous frame back on top.
    popFrameStack(tstate);

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_2:;
    CHECK_OBJECT(tmp_class_creation_1__bases);
    Py_DECREF(tmp_class_creation_1__bases);
    tmp_class_creation_1__bases = NULL;
    CHECK_OBJECT(tmp_class_creation_1__class_decl_dict);
    Py_DECREF(tmp_class_creation_1__class_decl_dict);
    tmp_class_creation_1__class_decl_dict = NULL;
    CHECK_OBJECT(tmp_class_creation_1__metaclass);
    Py_DECREF(tmp_class_creation_1__metaclass);
    tmp_class_creation_1__metaclass = NULL;
    CHECK_OBJECT(tmp_class_creation_1__prepared);
    Py_DECREF(tmp_class_creation_1__prepared);
    tmp_class_creation_1__prepared = NULL;

    // Report to PGO about leaving the module without error.
    PGO_onModuleExit("qtimgren$ui_profiles", false);

#if defined(_NUITKA_MODULE) && 0
    {
        PyObject *post_load = IMPORT_EMBEDDED_MODULE(tstate, "qtimgren.ui_profiles" "-postLoad");
        if (post_load == NULL) {
            return NULL;
        }
    }
#endif

    Py_INCREF(module_qtimgren$ui_profiles);
    return module_qtimgren$ui_profiles;
    module_exception_exit:

#if defined(_NUITKA_MODULE) && 0
    {
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_qtimgren$ui_profiles, (Nuitka_StringObject *)const_str_plain___name__);

        if (module_name != NULL) {
            Nuitka_DelModule(tstate, module_name);
        }
    }
#endif
    PGO_onModuleExit("qtimgren$ui_profiles", false);

    RESTORE_ERROR_OCCURRED_STATE(tstate, &exception_state);
    return NULL;
}
