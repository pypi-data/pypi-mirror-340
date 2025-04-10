import shutil
import os


curr_dir = os.path.dirname(os.path.abspath(__file__))


def _read_dcd_header(file):
    import struct

    with open(file, "r+b") as f:
        f.seek(8, os.SEEK_SET)
        numFrames = struct.unpack("<i", f.read(4))[0]
        f.seek(20, os.SEEK_SET)
        currStep = struct.unpack("<i", f.read(4))[0]
        return numFrames, currStep


def _test_structprep(tmp_path):
    from atm.rbfe_structprep import rbfe_structprep

    shutil.copytree(
        os.path.join(curr_dir, "QB_A08_A07"), os.path.join(tmp_path, "QB_A08_A07")
    )
    rbfe_structprep(os.path.join(tmp_path, "QB_A08_A07", "QB_A08_A07_asyncre.yaml"))


def _test_production(tmp_path):
    from atm.rbfe_production import rbfe_production

    shutil.copytree(
        os.path.join(curr_dir, "QB_A08_A07_completed"),
        os.path.join(tmp_path, "QB_A08_A07_completed"),
    )
    rbfe_production(
        os.path.join(tmp_path, "QB_A08_A07_completed", "QB_A08_A07_asyncre.yaml")
    )
    for i in range(4):
        assert os.path.exists(
            os.path.join(tmp_path, "QB_A08_A07_completed", f"r{i}", "QB_A08_A07.dcd")
        )


def _test_production_xtc(tmp_path):
    from atm.rbfe_production import rbfe_production
    import yaml

    shutil.copytree(
        os.path.join(curr_dir, "QB_A08_A07_completed"),
        os.path.join(tmp_path, "QB_A08_A07_completed"),
    )

    configfile = os.path.join(
        tmp_path, "QB_A08_A07_completed", "QB_A08_A07_asyncre.yaml"
    )
    with open(configfile, "r") as f:
        config = yaml.safe_load(f)
    config["XTC_TRAJECTORY"] = True
    with open(configfile, "w") as f:
        yaml.dump(config, f)

    rbfe_production(configfile)
    for i in range(4):
        assert os.path.exists(
            os.path.join(tmp_path, "QB_A08_A07_completed", f"r{i}", "QB_A08_A07.xtc")
        )


def _test_production_incremental(tmp_path):
    from atm.rbfe_production import rbfe_production
    import yaml

    shutil.copytree(
        os.path.join(curr_dir, "QB_A08_A07_completed"),
        os.path.join(tmp_path, "QB_A08_A07_completed"),
    )

    configfile = os.path.join(
        tmp_path, "QB_A08_A07_completed", "QB_A08_A07_asyncre.yaml"
    )
    with open(configfile, "r") as f:
        config = yaml.safe_load(f)
    config["MAX_SAMPLES"] = "+1"
    with open(configfile, "w") as f:
        yaml.dump(config, f)

    rbfe_production(configfile)
    for i in range(4):
        dcdf = os.path.join(tmp_path, "QB_A08_A07_completed", f"r{i}", "QB_A08_A07.dcd")
        numFrames, _ = _read_dcd_header(dcdf)
        assert numFrames == 1

    startsampl_file = os.path.join(tmp_path, "QB_A08_A07_completed", "starting_sample")
    with open(startsampl_file, "r") as f:
        starting_sample = int(f.read().strip())
        assert starting_sample == 1
    prog_file = os.path.join(tmp_path, "QB_A08_A07_completed", "progress")
    with open(prog_file, "r") as f:
        progress = float(f.read().strip())
        assert progress == 0.0

    # Run another 2 samples
    os.remove(startsampl_file)
    os.remove(prog_file)
    config["MAX_SAMPLES"] = "+2"
    with open(configfile, "w") as f:
        yaml.dump(config, f)
    rbfe_production(configfile)
    for i in range(4):
        dcdf = os.path.join(tmp_path, "QB_A08_A07_completed", f"r{i}", "QB_A08_A07.dcd")
        numFrames, _ = _read_dcd_header(dcdf)
        assert numFrames == 2

    with open(startsampl_file, "r") as f:
        starting_sample = int(f.read().strip())
        assert starting_sample == 2
    with open(prog_file, "r") as f:
        progress = float(f.read().strip())
        assert progress == 0.5


def _test_uwham_analysis(tmp_path):
    from atm.uwham import calculate_uwham

    shutil.copytree(
        os.path.join(curr_dir, "TYK2_A02_A09"), os.path.join(tmp_path, "TYK2_A02_A09")
    )

    run_dir = os.path.join(tmp_path, "TYK2_A02_A09", "TYK2_A02_A09_r0_1")
    ddG, ddG_std, dgbind1, dgbind2, samples = calculate_uwham(run_dir, "QB_A02_A09", 70)

    expected_ddG = -1.0582613105156682
    expected_ddG_std = 0.1967262793670161
    assert abs(ddG - expected_ddG) < 1e-8
    assert abs(ddG_std - expected_ddG_std) < 1e-8
    assert samples == 351
    assert abs(dgbind1 - 16.12549393024899) < 1e-8
    assert abs(dgbind2 - 17.183755240764658) < 1e-8

    run_dir = os.path.join(tmp_path, "TYK2_A02_A09", "TYK2_A02_A09_r0_2")
    ddG, ddG_std, dgbind1, dgbind2, samples = calculate_uwham(run_dir, "QB_A02_A09", 70)

    expected_ddG = -1.9492444343451716
    expected_ddG_std = 0.18548486855089807
    assert abs(ddG - expected_ddG) < 1e-8
    assert abs(ddG_std - expected_ddG_std) < 1e-8
    assert samples == 421
    assert abs(dgbind1 - 15.690178371190054) < 1e-8
    assert abs(dgbind2 - 17.639422805535226) < 1e-8

    run_dir = os.path.join(tmp_path, "TYK2_A02_A09", "TYK2_A02_A09_r0_3")
    ddG, ddG_std, dgbind1, dgbind2, samples = calculate_uwham(
        run_dir, "QB_A02_A09", None
    )

    expected_ddG = -1.2625416487680994
    expected_ddG_std = 0.2068400471106031
    assert abs(ddG - expected_ddG) < 1e-8
    assert abs(ddG_std - expected_ddG_std) < 1e-8
    assert samples == 480
    assert abs(dgbind1 - 16.159606073746524) < 1e-8
    assert abs(dgbind2 - 17.422147722514623) < 1e-8
