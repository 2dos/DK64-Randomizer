#include <assert.h>

#ifdef XDWORKAROUND
#define ssize_t ssize_t_wrap
#endif
#include "xdelta3.h"
#include "xdelta3.c"
#ifdef XDWORKAROUND
#undef ssize_t
#endif

#define MALLOC_CHECK(var) if (var == NULL) { PyErr_NoMemory(); return NULL; }

#include <Python.h>

static PyObject *method_run(PyObject *self, PyObject *args, PyObject *kwargs)
{
    char *infile = NULL;
    char *outfile = NULL;
    char *patchfile = NULL;

    static char *kwlist[] = {"infile", "outfile", "patchfile",
                                NULL};

    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "sss", kwlist,
                                    &infile, &outfile, &patchfile))
        return NULL;

    int argc = 7;
    char** argv = (char**)PyMem_Malloc(sizeof(char*) * (argc + 1));
    MALLOC_CHECK(argv);
    argv[0] = "xdelta3";
    argv[1] = "-f";
    argv[2] = "-e";
    argv[3] = "-s";
    argv[4] = infile;
    argv[5] = outfile;
    argv[6] = patchfile;
    argv[7] = NULL;
    int result = xd3_main_cmdline(argc, argv);
    PyMem_Free(argv);
    return PyBool_FromLong((long)(result == 0));
}

static PyMethodDef PyxdeltaMethods[] = {
    {"run", (PyCFunction)method_run, METH_VARARGS | METH_KEYWORDS, "Python interface for xdelta."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pyxdeltamodule = {
    PyModuleDef_HEAD_INIT,
    "pyxdelta",
    "Python interface for xdelta.",
    -1,
    PyxdeltaMethods
};

PyMODINIT_FUNC PyInit_pyxdelta(void)
{
    return PyModule_Create(&pyxdeltamodule);
}
