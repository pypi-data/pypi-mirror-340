import midii
import mido
from rich import print as rprint


def test_sample():
    print(midii.sample.real)
    print(midii.sample.dataset)
    print(midii.sample.simple)


def test_midii_simple_print_tracks():
    ma = midii.MidiFile(midii.sample.simple[0])
    ma.quantize(unit="256")
    ma.print_tracks()


def test_midii_real_print_tracks():
    ma = midii.MidiFile(midii.sample.real[1])
    ma.quantize(unit="256")
    ma.print_tracks(print_note_info=True, track_list=["piano-r"])


def test_mido_dataset_print_tracks():
    ma = mido.MidiFile(midii.sample.dataset[1])
    ma.print_tracks()


def test_midii_print_tracks():
    ma = midii.MidiFile(
        midii.sample.dataset[1], convert_1_to_0=True, lyric_encoding="cp949"
    )
    ma.quantize(unit="32")
    ma.print_tracks()


def test_midii_quantize():
    ma = midii.MidiFile(
        midii.sample.dataset[1], convert_1_to_0=True, lyric_encoding="cp949"
    )
    ma.quantize(unit="32")
    ma.print_tracks()


def test_version():
    from importlib.metadata import version
    import platform

    print("Python Version (concise):", platform.python_version())
    print("mido version:", version("mido"))
    print("rich version:", version("rich"))


def test_midii_print_times():
    ma = midii.MidiFile(
        midii.sample.dataset[0], convert_1_to_0=True, lyric_encoding="cp949"
    )
    ma.print_tracks()


def test_to_json():
    ma = midii.MidiFile(
        midii.sample.dataset[0], convert_1_to_0=True, lyric_encoding="cp949"
    )
    rprint(ma.to_json())
    ma.quantize()
    rprint(ma.to_json())


def test_lyrics():
    ma = midii.MidiFile(
        midii.sample.dataset[0], convert_1_to_0=True, lyric_encoding="cp949"
    )
    print(ma.lyrics)


def test_times():
    ma = midii.MidiFile(
        midii.sample.dataset[0], convert_1_to_0=True, lyric_encoding="cp949"
    )
    print(ma.times)
    ma.quantize()
    print(ma.times)


if __name__ == "__main__":
    # test_sample()
    # test_midii_simple_print_tracks()
    # test_midii_real_print_tracks()
    # test_mido_dataset_print_tracks()
    # test_midii_print_tracks()
    # test_midii_quantize()
    # test_midii_print_times()
    # test_version()
    # test_to_json()
    # test_lyrics()
    test_times()
