from pprint import pprint

from camtasio.utils.color import RGBA
from camtasio.effects.chroma_key import ChromaKeyEffect
# TODO: Add EffectSchema when available
# from camtasio.effects import EffectSchema


def test_create_default_chromakey_effect():
    ChromaKeyEffect()


def test_default_chromakey_effect_parameters():
    effect = ChromaKeyEffect()
    assert effect.tolerance == effect.parameters.tolerance


def test_construct_chromakey_effect_with_rgba():
    expected = RGBA(255, 127, 63, 31)
    effect = ChromaKeyEffect(hue=expected)
    assert effect.hue == expected


def test_construct_chromakey_effect_with_hex():
    color = "#FF7F3F1F"
    expected = RGBA(255, 127, 63, 31)
    effect = ChromaKeyEffect(hue=color)
    assert effect.hue == expected


# TODO: Re-enable these tests when EffectSchema is implemented
# def test_serialize_default_chromakey_effect_to_dictionary():
#     effect = ChromaKeyEffect()
#     schema = EffectSchema()
#     actual = schema.dump(effect)
#     pprint(actual)
#     expected = {
#         'effectName': 'ChromaKey',
#         'category': 'categoryVisualEffects',
#         'parameters': {
#             'clrCompensation': 0.0,
#             'color-alpha': 1.0,
#             'color-blue': 0.0,
#             'color-green': 1.0,
#             'color-red': 0.0,
#             'defringe': 0.0,
#             'enabled': 1,
#             'invertEffect': 0.0,
#             'softness': 0.1,
#             'tolerance': 0.1,
#         }
#     }
#     assert actual == expected


def test_default_chromakey_effect_metadata():
    effect = ChromaKeyEffect()
    actual = effect.metadata
    expected = {
        "default-ChromaKey-color" : "(0,255,0,255)",
        "default-ChromaKey-defringe" : "0",
        "default-ChromaKey-invertEffect" : "0",
        "default-ChromaKey-softness" : "0.1",
        "default-ChromaKey-tolerance" : "0.1",
        "default-ChromaKey-clrCompensation": "0",
    }
    assert actual == expected



