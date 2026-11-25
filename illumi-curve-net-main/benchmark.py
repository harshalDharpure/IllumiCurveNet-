import csv
from pathlib import Path
import numpy as np
import torch
from PIL import Image
from pyiqa import create_metric
import model

torch.set_num_threads(4)
paths = sorted(Path("data/test_data/PSR").glob("*.TIF"))
assert len(paths) == 40
out = Path("data/result/PSR")
out.mkdir(parents=True, exist_ok=True)
net = model.illumi_curve_net().cuda()
net.load_state_dict(torch.load("snapshots/model-best.pth", weights_only=True))
metrics = {name: create_metric(name, device="cpu") for name in ("piqe", "niqe", "brisque")}
# PyIQA 0.1.13 transposes the support vectors in place during scoring.
support_vectors = metrics["brisque"].net.sv.clone()

def to_tensor(pixels):
    return torch.from_numpy(np.asarray(pixels) / 255.0).float().permute(2, 0, 1).unsqueeze(0)

rows = []
with torch.inference_mode():
    for index, path in enumerate(paths, 1):
        with Image.open(path) as image:
            raw = to_tensor(image)
        enhanced, _ = net(raw.cuda())
        pixels = (enhanced[0].permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
        Image.fromarray(pixels).save(out / (path.stem + ".png"))
        row = {"image": path.name}
        for kind, tensor in (("raw", raw), ("enhanced", to_tensor(pixels))):
            for name, metric in metrics.items():
                if name == "brisque":
                    metric.net.sv = support_vectors.clone()
                row[f"{kind}_{name}"] = metric(tensor).item()
        rows.append(row)
        if index % 10 == 0:
            print(f"Scored {index}/40")
columns = list(rows[0])
scores = np.array([[row[key] for key in columns[1:]] for row in rows])
assert np.isfinite(scores).all()
assert len(list(out.glob("*.png"))) == 40
with (out / "scores.csv").open("w", newline="") as stream:
    writer = csv.DictWriter(stream, columns)
    writer.writeheader()
    writer.writerows(rows)
print(dict(zip(columns[1:], scores.mean(axis=0).tolist())))
