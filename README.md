# CSV tag data for a1111-sd-webui-tagcomplete based on animagine-xl-3.0 dataset

3 files that help to input tags on [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) for generating image via [animagine-xl-3.0](https://huggingface.co/cagliostrolab/animagine-xl-3.0)

- [animagine-xl-3.0.csv](outputs/animagine-xl-3.0.csv) : tag data file for [a1111-sd-webui-tagcomplete](https://github.com/DominikDoom/a1111-sd-webui-tagcomplete)
- [character_plus.txt](outputs/character_plus.txt) : character wildcards
- [animagine_xl_3.0_artists.txt](outputs/animagine_xl_3.0_artists.txt) : artist wildcards

You can modify or create new using ipynb files.


## animagine-xl-3.0.csv

A tag data file from [Linaqruf/1.2m-ordered-tags](https://huggingface.co/datasets/Linaqruf/1.2m-ordered-tags) dataset, which I believe the data for training animagine-xl-3.0.

### Usage

1. Put file on `extensions/a1111-sd-webui-tagcomplete/tags`.
2. Select animagine-xl-3.0.csv' on **Settings > Tag Autocomplete > Tag filename**, then press apply button.
3. Type on prompt.

![image](https://github.com/bedovyy/tagcomplete-for-animagine-xl-3.0/assets/137917911/e6071a3f-7335-4d54-b261-5321b570998a)


## character_plus.txt & animagine_xl_3.0_artists.txt

Wildcard files for character tags and artist tags, that
- based on chracter wildcards from [Linaqruf/animagine-xl](https://huggingface.co/spaces/Linaqruf/animagine-xl) space, and I add 10 tags mostly used with each characters.
- about 1000 mostly used artist tags and 10 additional tags that mostly used with.

### Usage

1. Put files on valid wildcards location. \
   (In case of [sd-dynamic-prompts](https://github.com/adieyal/sd-dynamic-prompts), it's `extensions/sd-dynamic-prompts/wildcards`.)
2. Input `__character_plus__` or `__animagine_xl_3.0_artists__` on prompt and generate.
3. [a1111-sd-webui-tagcomplete](https://github.com/DominikDoom/a1111-sd-webui-tagcomplete) may helps to input wildcard on prompt.

![image](https://github.com/bedovyy/tagcomplete-for-animagine-xl-3.0/assets/137917911/669eaf28-2f4c-4e09-b336-070f4b50f361)
