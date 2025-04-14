#include "pairwise_hist_one_byte_5bit.cuh"

using namespace cooperative_groups;

namespace NKernel {

    template
    void ComputePairwiseHistogramOneByte5BitsImpl<true>(const TCFeature* features, const TCFeature* featuresCpu,
                                                        const ui32 featureCount,
                                                        const ui32 fiveBitsFeatureCount,
                                                        const ui32* compressedIndex,
                                                        const uint2* pairs, ui32 pairCount,
                                                        const float* weight,
                                                        const TDataPartition* partition,
                                                        ui32 partCount,
                                                        ui32 histLineSize,
                                                        bool fullPass,
                                                        float* histogram,
                                                        int parallelStreams,
                                                        TCudaStream stream);


}
