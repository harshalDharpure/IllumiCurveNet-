# IllumiCurveNet benchmark reproduction

This repository documents a local evaluation of the published IllumiCurveNet checkpoint on the 40-image ZSPL-PSR lunar benchmark.

| Item | Link |
| --- | --- |
| Reproduction report | [RESULTS.md](RESULTS.md) |
| Model, training and inference code | [IllumiCurveNet source](illumi-curve-net-main) |
| Raw and enhanced metrics for all 40 images | [scores.csv](illumi-curve-net-main/data/result/PSR/scores.csv) |
| Benchmark outputs | [40 enhanced images](illumi-curve-net-main/data/result/PSR) |
| Visual example | [Before and after](illumi-curve-net-main/data/result/paper-figure-1/before-after.png) |

## Run the benchmark

1. Follow the [project installation instructions](illumi-curve-net-main/README.md#installation), including a CUDA-enabled PyTorch installation and the pinned PyIQA dependency.
2. Download [comtestSN.zip](https://github.com/dl-zfq/PSR_Enhancement/tree/HEAD/test_set) and place the 40 TIFFs directly in `illumi-curve-net-main/data/test_data/PSR/`.
3. Run `python benchmark.py` from `illumi-curve-net-main/`. The script saves enhanced images and per-image scores in `data/result/PSR/`.

The [upstream IllumiCurveNet repository](https://github.com/JustSurWHYving/illumi-curve-net) provides the original implementation and checkpoint. See the included [license](illumi-curve-net-main/LICENSE).
