#include <catboost/cuda/cuda_util/kernel/sort_templ.cuh>

namespace NKernel {
    template cudaError_t RadixSort(ui64* keys, uchar* values, ui32 size, TRadixSortContext& context,  TCudaStream stream);
}
