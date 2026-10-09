# Expanded motion-guidance robustness study

**Completed:** 16 diverse test-image views × 19 conditions = 304 measurements. **Unresolved:** exact reconstruction of the authors’ supplied motion fields from the released raw gyro. Accordingly, the controlled perturbations below are motion-field stress tests, not a validated physical sensor-error or timing-offset study.

## Main finding

With image pixels and network weights held fixed, reducing, enlarging, reversing or rotating the motion guidance changes sharp-reference feature recovery. Larger tested distortions generally reduce both mean reconstruction quality and correct recovered matches. This establishes input sensitivity on this selected sample. It does not establish novelty, causal benefit over a trained image-only ablation, independent inter-frame matching performance, or SLAM reliability.

## Broader baseline comparison

The fixed sample is IDs 000001, 000041, …, 000601 from the 640-image test split, selected before inference. Contact-sheet inspection confirms varied street, text, foliage and building views. Some views share a location or subject; original capture/sequence independence is not verified. This is broader than the previous single-background test, but not a random or statistically independent scene benchmark. One image overlaps the previous sample.

| Method | Mean linear PSNR (dB) | Mean SSIM | Mean correct sharp-reference matches | Mean precision on nonempty match sets | Nonempty sets |
|---|---:|---:|---:|---:|---:|
| raw | 20.15 | 0.3640 | 0.06 | 0.022 | 15/16 |
| gyro | 27.18 | 0.7706 | 37.88 | 0.651 | 16/16 |
| restormer_direct | 19.90 | 0.3655 | 0.44 | 0.043 | 13/16 |
| restormer_gamma_bridge | 19.52 | 0.3200 | 0.00 | 0.000 | 16/16 |

GyroDeblurNet was trained on GyroBlur-Synth; Restormer was trained on GoPro. This domain/architecture difference and unresolved color-domain equivalence prevent attribution of the ranking solely to gyro. Direct and fixed power-1/2.2 bridge variants are both retained. The bridge did not improve this sample’s mean results; it was not selected or tuned using outcomes.

## Controlled motion-field perturbations

| Condition | Mean PSNR (dB) | Mean correct matches | Images with fewer correct matches than supplied-field baseline | Mean paired match change |
|---|---:|---:|---:|---:|
| Supplied motion field | 27.18 | 37.88 | 0/16 | +0.00 |
| Reconstructed field — diagnostic | 27.39 | 39.06 | 4/16 | +1.19 |
| Zero field — missing-input stress | 21.30 | 3.50 | 16/16 | -34.38 |
| 50% scale | 24.21 | 15.25 | 16/16 | -22.62 |
| 75% scale | 26.95 | 33.38 | 13/16 | -4.50 |
| 125% scale | 26.64 | 30.25 | 13/16 | -7.62 |
| 150% scale | 25.35 | 19.12 | 16/16 | -18.75 |
| Reversed vectors | 21.90 | 3.44 | 16/16 | -34.44 |
| 5° image-plane vector rotation | 27.05 | 35.62 | 10/16 | -2.25 |
| 15° image-plane vector rotation | 26.27 | 26.69 | 15/16 | -11.19 |
| Additive .25-pixel field error, 3 seeds | 27.04 | 37.04 | 10/16 | -0.83 |
| Additive 1-pixel field error, 3 seeds | 26.16 | 29.38 | 16/16 | -8.50 |

The noisy conditions average three seeds within each image before aggregating across the 16 images. Seed replicates are not counted as independent scenes. No statistical significance or confidence interval is claimed.

Scaling multiplies the 16-channel field values. Direction tests rotate each of its eight XY segment vectors in the image plane. Additive error draws one Gaussian offset per channel, shared over spatial positions, with standard deviation .25 or 1 original-image pixel per segment. This preserves spatial smoothness; it is not a calibrated gyro noise process in rad/s. Vector rotation is not equivalent to a 3D camera–IMU extrinsic rotation. Zero and reversed fields are stress controls, not trained image-only baselines. No blurred image, model weight, crop or metric threshold changes between these conditions.

## Raw-gyro conversion validation

The adapter preserves the pinned official generator’s intrinsics, rotation signs, temporal interpolation, eight integration intervals, coordinate grid and channel order. Executing the original function bodies independently on the same first-sample crop gave a maximum absolute difference of **0.0** from the adapter; a zero-motion test also passed. This verifies implementation agreement for the checked case, not correctness of the authors’ data-generation provenance.

Across the original 16 samples, reconstructed versus supplied fields had mean absolute difference **0.5593 pixels per field component** using the listed start as a zero-based index; maximum component discrepancy across those samples was **1.6280 pixels**. Adjacent start-index conventions did not resolve it: mean errors were .7669 for index−1 and .8274 for index+1. The downloaded dataset gyro and repository gyro have identical numeric values, despite different file bytes/line endings. Therefore, the mismatch is not resolved by choosing the other raw copy or shifting the index by one.

The authors state that the released generator creates unperturbed fields. A supplied-field perturbation, differing generation details or calibration could explain the mismatch, but none is confirmed. We did not fit camera parameters or select offsets to maximize test performance. The reconstructed-field row above is an explicit diagnostic, not a validated replacement for the supplied baseline. Its slightly different performance does not validate the reconstruction.

**Consequent limit:** physically parameterized timing offsets, angular-velocity bias/noise and camera–IMU calibration sweeps remain uncompleted. Before those claims, obtain the exact supplied-field perturbation/generation settings or a verified image–gyro calibration and synthesis pipeline. Do not rename the field-scale/rotation tests as those physical experiments.

## Protocol and verification

Both models process the same central 256×256 crop. The corresponding 128×128×16 field is cropped without resizing or changing vector units. Quality metrics exclude a 24-pixel border. ORB uses a fixed 500-keypoint cap, FAST .05, cross-checked Hamming matches, ratio .8 and 2-pixel geometric tolerance. Correctness is against the same image’s sharp reference under the identity map. Results therefore measure sharp-feature recovery, not temporal tracking. The reference is never a neural input. Zero-match cases are retained with undefined precision.

Source commits, weights and input hashes were checked; strict model loading, finite input/output shapes, blank-feature handling and sharp self-matching passed. All 304 sample/condition records are unique and correct matches never exceed returned matches. The fixed protocol was saved before model execution. The output arrays, per-sample CSV, settings and protocol permit inspection and reproduction. Forward timing excludes preprocessing, transfer, I/O and features; no real-time robotics claim follows.

## Decision for the project

Continue with task-quality sensitivity and failure analysis. This work now has executable baselines, a broader image sample, controlled field-level stress measurements and a concrete reproducibility issue to resolve. A sensor-error sweep alone remains existing research, so novelty must come from a demonstrably different question, protocol or method compared with the closest prior work.

Next technical gate: resolve the supplied-field mismatch, recover source-scene IDs for splitting, and establish independent inter-frame geometric truth. Then freeze sensor-error ranges using training/validation information. Do not move to a selector or SLAM experiment on the strength of these crop-level results alone.

## Public release scope

The accompanying CSV, summary, protocol and settings document the completed local experiment. Run `python scripts/verify_results.py` from the repository root to check record completeness and aggregate results. Full neural inference code and input artifacts are not part of this initial public release; local output-array validation is documented in `final_validation.json`.

Official implementations are linked in the repository's `REFERENCES.md`.
