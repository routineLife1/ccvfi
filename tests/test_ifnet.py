import cv2

from ccvfi import AutoConfig, AutoModel, BaseConfig, ConfigType
from ccvfi.model import VFIBaseModel

from .util import ASSETS_PATH, calculate_image_similarity, get_device, load_eval_image, load_images


class Test_IFNet:
    def test_official(self) -> None:
        img0, img1, _ = load_images()
        eval_img = load_eval_image()

        for k in [ConfigType.IFNet_v426_heavy]:
            print(f"Testing {k}")
            cfg: BaseConfig = AutoConfig.from_pretrained(k)
            model: VFIBaseModel = AutoModel.from_config(config=cfg, fp16=False, device=get_device())
            print(model.device)

            out = model.inference_image_list(img_list=[img0, img1])

            assert len(out) == 1
            for img in out:
                cv2.imwrite(str(ASSETS_PATH / f"test_{k}_out.jpg"), img)
                assert calculate_image_similarity(eval_img, img)
