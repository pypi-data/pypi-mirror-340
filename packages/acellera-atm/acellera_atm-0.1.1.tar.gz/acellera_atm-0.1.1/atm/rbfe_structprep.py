import sys
import time
import logging
from sys import stdout
import openmm as mm
import openmm.app as app
from openmm.unit import kelvin, bar, kilocalorie_per_mole, kilojoules_per_mole
from atm.ommsystem import OMMSystemAmberRBFE
from atm.atomutils import AtomUtils

logger = logging.getLogger(__name__)


class OMMSystemAmberRBFEnoATM(OMMSystemAmberRBFE):
    def create_system(self):

        self.load_amber_system()
        self.atm_utils = AtomUtils(self.system)
        self.set_ligand_atoms()
        self.set_displacement()
        self.set_vsite_restraints()
        # set orientation restraints
        self.set_orientation_restraints()
        # set reference atoms for alignment force
        self.set_alignmentForce()
        # indexes of the atoms whose position is restrained near the initial positions
        # by a flat-bottom harmonic potential.
        self.set_positional_restraints()

        # target temperature
        temp = self.keywords.get("TEMPERATURES")
        if temp is None:
            self.temperature = 300.0 * kelvin
        elif isinstance(temp, list):
            self.temperature = float(temp[0]) * kelvin
        else:
            self.temperature = float(temp) * kelvin

        self.set_torsion_metaDbias(self.temperature)

        # do not include ATM Force, instead place the nonbonded
        # forces in what it would be the the ATMForce group
        # for the integrator
        # self.set_atmforce()
        self.atmforcegroup = self.nonbondedforcegroup  # for integrator

        self.atmforcegroup = self.free_force_group()
        import re

        nbpattern = re.compile(".*Nonbonded.*")
        for i in range(self.system.getNumForces()):
            if nbpattern.match(str(type(self.system.getForce(i)))):
                nbforce = self.system.getForce(i)
                nbforce.setForceGroup(self.atmforcegroup)
                break

        # add barostat
        pressure = 1 * bar
        self.set_barostat(self.temperature, pressure, 25)

        self.set_integrator(self.temperature, self.frictionCoeff, self.MDstepsize)


def do_mintherm(keywords, logger):
    basename = keywords.get("BASENAME")
    jobname = basename

    prmtopfile = basename + ".prmtop"
    crdfile = basename + ".inpcrd"

    # OpenMM system for minimization, thermalization, NPT, NVT
    # does not include ATM Force
    syst = OMMSystemAmberRBFEnoATM(basename, keywords, prmtopfile, crdfile, logger)
    syst.create_system()

    platform_properties = {}
    platform_name = keywords.get("OPENMM_PLATFORM")
    if platform_name is None:
        platform_name = "CUDA"
    if platform_name == "CUDA" or platform_name == "OpenCL" or platform_name == "HIP":
        platform_properties["Precision"] = "mixed"
    platform = mm.Platform.getPlatformByName(platform_name)

    simulation = app.Simulation(
        syst.topology, syst.system, syst.integrator, platform, platform_properties
    )
    simulation.context.setPositions(syst.positions)
    if syst.inpcrd.boxVectors is not None:
        simulation.context.setPeriodicBoxVectors(*syst.inpcrd.boxVectors)

    print("Using platform %s" % simulation.context.getPlatform().getName())

    print(
        "Potential energy before minimization =",
        simulation.context.getState(getEnergy=True).getPotentialEnergy(),
    )
    print("Energy minimizing the system ...")
    simulation.minimizeEnergy()
    print(
        "Potential energy after minimization =",
        simulation.context.getState(getEnergy=True).getPotentialEnergy(),
    )

    # saves minimization checkpoint
    simulation.saveState(jobname + "_min.xml")
    # saves a pdb file
    positions = simulation.context.getState(getPositions=True).getPositions()
    boxsize = simulation.context.getState().getPeriodicBoxVectors()
    simulation.topology.setPeriodicBoxVectors(boxsize)
    with open(jobname + "_min.pdb", "w") as output:
        app.PDBFile.writeFile(simulation.topology, positions, output)

    print("Thermalization ...")

    totalSteps = int(keywords.get("EQUIL_MINIM_STEPS", 150000))
    steps_per_cycle = int(keywords.get("STEPS_PER_CYCLE", 5000))
    number_of_cycles = int(totalSteps / steps_per_cycle)
    simulation.reporters.append(
        app.StateDataReporter(
            stdout,
            steps_per_cycle,
            step=True,
            potentialEnergy=True,
            temperature=True,
            volume=True,
        )
    )

    # initial temperature
    initial_temp = keywords.get("INITIAL_TEMPERATURE")
    if initial_temp is None:
        initial_temperature = 50.0 * kelvin
    else:
        initial_temperature = float(initial_temp) * kelvin

    final_temperature = syst.temperature
    delta_temperature = (final_temperature - initial_temperature) / number_of_cycles

    syst.barostat.setFrequency(999999999)  # disabled

    # MD with temperature ramp
    temperature = initial_temperature
    syst.integrator.setTemperature(temperature)
    for i in range(number_of_cycles):
        simulation.step(steps_per_cycle)
        # prepare system for new temperature
        temperature = temperature + delta_temperature
        syst.integrator.setTemperature(temperature)

    # saves thermalized checkpoint
    simulation.saveState(jobname + "_therm.xml")
    # saves a pdb file
    positions = simulation.context.getState(getPositions=True).getPositions()
    boxsize = simulation.context.getState().getPeriodicBoxVectors()
    simulation.topology.setPeriodicBoxVectors(boxsize)
    with open(jobname + "_therm.pdb", "w") as output:
        app.PDBFile.writeFile(simulation.topology, positions, output)

    print("NPT equilibration ...")

    syst.barostat.setFrequency(25)

    for i in range(number_of_cycles):
        simulation.step(steps_per_cycle)

    # saves checkpoint
    simulation.saveState(jobname + "_npt.xml")
    # saves a pdb file
    positions = simulation.context.getState(getPositions=True).getPositions()
    boxsize = simulation.context.getState().getPeriodicBoxVectors()
    simulation.topology.setPeriodicBoxVectors(boxsize)
    with open(jobname + "_npt.pdb", "w") as output:
        app.PDBFile.writeFile(simulation.topology, positions, output)

    print("NVT equilibration ...")
    syst.barostat.setFrequency(999999999)  # disabled

    # MD at constant volume
    for i in range(number_of_cycles):
        simulation.step(steps_per_cycle)

    # saves checkpoint
    simulation.saveState(jobname + "_equil.xml")
    # saves a pdb file
    positions = simulation.context.getState(getPositions=True).getPositions()
    boxsize = simulation.context.getState().getPeriodicBoxVectors()
    simulation.topology.setPeriodicBoxVectors(boxsize)
    with open(jobname + "_equil.pdb", "w") as output:
        app.PDBFile.writeFile(simulation.topology, positions, output)


def do_lambda_annealing(keywords, logger):
    basename = keywords.get("BASENAME")
    jobname = basename

    prmtopfile = basename + ".prmtop"
    crdfile = basename + ".inpcrd"

    syst = OMMSystemAmberRBFE(basename, keywords, prmtopfile, crdfile, logger)
    syst.create_system()

    platform_properties = {}
    platform_name = keywords.get("OPENMM_PLATFORM")
    if platform_name is None:
        platform_name = "CUDA"
    if platform_name == "CUDA" or platform_name == "OpenCL" or platform_name == "HIP":
        platform_properties["Precision"] = "mixed"
    platform = mm.Platform.getPlatformByName(platform_name)

    simulation = app.Simulation(
        syst.topology, syst.system, syst.integrator, platform, platform_properties
    )
    simulation.context.setPositions(syst.positions)
    if syst.inpcrd.boxVectors is not None:
        simulation.context.setPeriodicBoxVectors(*syst.inpcrd.boxVectors)

    print("Using platform %s" % simulation.context.getPlatform().getName())

    syst.barostat.setFrequency(999999999)  # disabled

    # target temperature
    temp = keywords.get("TEMPERATURES")
    if temp is None:
        temperature = 300.0 * kelvin
    elif isinstance(temp, list):
        temperature = float(temp[0]) * kelvin
    else:
        temperature = float(temp) * kelvin

    lmbd = 0.0
    lambda1 = lmbd
    lambda2 = lmbd
    alpha = 0.0 / kilocalorie_per_mole
    uh = 0.0 * kilocalorie_per_mole
    w0coeff = 0.0 * kilocalorie_per_mole
    umsc = 1000.0 * kilocalorie_per_mole
    ubcore = 500.0 * kilocalorie_per_mole
    acore = 0.062500
    direction = 1

    print("LoadState ...")
    simulation.loadState(jobname + "_equil.xml")

    # override ATM parameters
    simulation.context.setParameter(syst.atmforce.Lambda1(), lambda1)
    simulation.context.setParameter(syst.atmforce.Lambda2(), lambda2)
    simulation.context.setParameter(syst.atmforce.Alpha(), alpha * kilojoules_per_mole)
    simulation.context.setParameter(syst.atmforce.Uh(), uh / kilojoules_per_mole)
    simulation.context.setParameter(syst.atmforce.W0(), w0coeff / kilojoules_per_mole)
    simulation.context.setParameter(syst.atmforce.Umax(), umsc / kilojoules_per_mole)
    simulation.context.setParameter(
        syst.atmforce.Ubcore(), ubcore / kilojoules_per_mole
    )
    simulation.context.setParameter(syst.atmforce.Acore(), acore)
    simulation.context.setParameter(syst.atmforce.Direction(), direction)

    if syst.doMetaD:
        fgroups = {0, syst.metaDforcegroup, syst.atmforcegroup}
    else:
        fgroups = {0, syst.atmforcegroup}

    state = simulation.context.getState(getEnergy=True)
    # print("Potential Energy =", state.getPotentialEnergy())

    print("Annealing to lambda = 1/2 ...")

    totalSteps = int(keywords.get("EQUIL_ANNEALING_STEPS", 250000))
    steps_per_cycle = int(keywords.get("STEPS_PER_CYCLE", 5000))
    number_of_cycles = int(totalSteps / steps_per_cycle)
    deltalambda = (0.5 - 0.0) / float(number_of_cycles)
    simulation.reporters.append(
        app.StateDataReporter(
            stdout, steps_per_cycle, step=True, potentialEnergy=True, temperature=True
        )
    )
    simulation.reporters.append(
        app.DCDReporter(jobname + "_mdlambda.dcd", steps_per_cycle)
    )

    state = simulation.context.getState(getEnergy=True, groups=fgroups)
    print("Potential Energy =", state.getPotentialEnergy())

    binding_file = jobname + "_mdlambda.out"
    f = open(binding_file, "w")

    for i in range(number_of_cycles):
        simulation.step(steps_per_cycle)
        state = simulation.context.getState(getEnergy=True)
        pot_energy = state.getPotentialEnergy()
        (u1, u0, ebias) = syst.atmforce.getPerturbationEnergy(simulation.context)
        umcore = (
            simulation.context.getParameter(syst.atmforce.Umax()) * kilojoules_per_mole
        )
        ubcore = (
            simulation.context.getParameter(syst.atmforce.Ubcore())
            * kilojoules_per_mole
        )
        acore = simulation.context.getParameter(syst.atmforce.Acore())
        direction = simulation.context.getParameter(syst.atmforce.Direction())
        if direction > 0:
            pert_energy = syst.atm_utils.softCorePertE(u1 - u0, umcore, ubcore, acore)
        else:
            pert_energy = syst.atm_utils.softCorePertE(u0 - u1, umcore, ubcore, acore)
        l1 = simulation.context.getParameter(syst.atmforce.Lambda1())
        l2 = simulation.context.getParameter(syst.atmforce.Lambda2())
        a = simulation.context.getParameter(syst.atmforce.Alpha()) / kilojoules_per_mole
        umid = simulation.context.getParameter(syst.atmforce.Uh()) * kilojoules_per_mole
        w0 = simulation.context.getParameter(syst.atmforce.W0()) * kilojoules_per_mole
        print(
            "%f %f %f %f %f %f %f %f %f"
            % (
                temperature / kelvin,
                lmbd,
                l1,
                l2,
                a * kilocalorie_per_mole,
                umid / kilocalorie_per_mole,
                w0 / kilocalorie_per_mole,
                pot_energy / kilocalorie_per_mole,
                pert_energy / kilocalorie_per_mole,
            ),
            file=f,
        )
        f.flush()
        lmbd += deltalambda
        lambda1 += deltalambda
        lambda2 += deltalambda
        simulation.context.setParameter(syst.atmforce.Lambda1(), lambda1)
        simulation.context.setParameter(syst.atmforce.Lambda2(), lambda2)

    f.close()

    print("SaveState ...")
    simulation.saveState(jobname + "_mdlambda.xml")

    # saves a pdb file
    positions = simulation.context.getState(getPositions=True).getPositions()
    boxsize = simulation.context.getState().getPeriodicBoxVectors()
    simulation.topology.setPeriodicBoxVectors(boxsize)
    with open(jobname + "_mdlambda.pdb", "w") as output:
        app.PDBFile.writeFile(simulation.topology, positions, output)


def do_equil(keywords, logger):
    basename = keywords.get("BASENAME")
    jobname = basename

    prmtopfile = basename + ".prmtop"
    crdfile = basename + ".inpcrd"

    syst = OMMSystemAmberRBFE(basename, keywords, prmtopfile, crdfile, logger)
    syst.create_system()

    platform_properties = {}
    platform_name = keywords.get("OPENMM_PLATFORM")
    if platform_name is None:
        platform_name = "CUDA"
    if platform_name == "CUDA" or platform_name == "OpenCL" or platform_name == "HIP":
        platform_properties["Precision"] = "mixed"
    platform = mm.Platform.getPlatformByName(platform_name)

    simulation = app.Simulation(
        syst.topology, syst.system, syst.integrator, platform, platform_properties
    )
    simulation.context.setPositions(syst.positions)
    if syst.inpcrd.boxVectors is not None:
        simulation.context.setPeriodicBoxVectors(*syst.inpcrd.boxVectors)

    print("Using platform %s" % simulation.context.getPlatform().getName())

    syst.barostat.setFrequency(999999999)  # disabled

    # # target temperature
    # temp = keywords.get("TEMPERATURES")
    # if temp is None:
    #     temperature = 300.0 * kelvin
    # elif isinstance(temp, list):
    #     temperature = float(temp[0]) * kelvin
    # else:
    #     temperature = float(temp) * kelvin

    lmbd = 0.5
    lambda1 = lmbd
    lambda2 = lmbd
    alpha = 0.0 / kilocalorie_per_mole
    uh = 0.0 * kilocalorie_per_mole
    w0coeff = 0.0 * kilocalorie_per_mole
    umsc = 1000.0 * kilocalorie_per_mole
    ubcore = 500.0 * kilocalorie_per_mole
    acore = 0.062500
    direction = 1

    print("LoadState ...")
    simulation.loadState(jobname + "_mdlambda.xml")

    # override ATM parameters
    simulation.context.setParameter(syst.atmforce.Lambda1(), lambda1)
    simulation.context.setParameter(syst.atmforce.Lambda2(), lambda2)
    simulation.context.setParameter(syst.atmforce.Alpha(), alpha * kilojoules_per_mole)
    simulation.context.setParameter(syst.atmforce.Uh(), uh / kilojoules_per_mole)
    simulation.context.setParameter(syst.atmforce.W0(), w0coeff / kilojoules_per_mole)
    simulation.context.setParameter(syst.atmforce.Umax(), umsc / kilojoules_per_mole)
    simulation.context.setParameter(
        syst.atmforce.Ubcore(), ubcore / kilojoules_per_mole
    )
    simulation.context.setParameter(syst.atmforce.Acore(), acore)
    simulation.context.setParameter(syst.atmforce.Direction(), direction)

    # if syst.doMetaD:
    #     fgroups = {0, syst.metaDforcegroup, syst.atmforcegroup}
    # else:
    #     fgroups = {0, syst.atmforcegroup}

    state = simulation.context.getState(getEnergy=True)
    # print("Potential Energy =", state.getPotentialEnergy())

    print("Equilibration at lambda = 1/2 ...")

    totalSteps = int(keywords.get("EQUIL_STEPS", 150000))
    steps_per_cycle = int(keywords.get("STEPS_PER_CYCLE", 5000))
    simulation.reporters.append(
        app.StateDataReporter(
            stdout, steps_per_cycle, step=True, potentialEnergy=True, temperature=True
        )
    )
    simulation.reporters.append(app.DCDReporter(jobname + "_0.dcd", steps_per_cycle))

    state = simulation.context.getState(getEnergy=True)
    print("Potential Energy =", state.getPotentialEnergy())

    simulation.step(totalSteps)

    print("SaveState ...")
    simulation.saveState(jobname + "_0.xml")

    # saves a pdb file
    positions = simulation.context.getState(getPositions=True).getPositions()
    boxsize = simulation.context.getState().getPeriodicBoxVectors()
    simulation.topology.setPeriodicBoxVectors(boxsize)
    with open(jobname + "_0.pdb", "w") as output:
        app.PDBFile.writeFile(simulation.topology, positions, output)


def massage_keywords(keywords, restrain_solutes=True):

    # use 1 fs time step
    keywords["TIME_STEP"] = 0.001

    # restrain all solutes: receptor and ligands
    nlig2 = len(keywords.get("LIGAND2_ATOMS"))
    last_lig2_atom = int(keywords.get("LIGAND2_ATOMS")[nlig2 - 1])
    keywords["POS_RESTRAINED_ATOMS"] = [i for i in range(last_lig2_atom + 1)]


def rbfe_structprep(config_file=None):
    from atm.utils import set_directory
    from pathlib import Path
    import yaml
    import json

    if config_file is None:
        config_file = sys.argv[1]

    print("")
    print("========================================")
    print("AToM RBFE Structure Preparation         ")
    print("========================================")
    print("")
    print("Started at: " + str(time.asctime()))
    print("Input file:", config_file)
    print("")
    sys.stdout.flush()

    if config_file.endswith(".yaml"):
        with open(config_file, "r") as f:
            keywords = yaml.safe_load(f)
    elif config_file.endswith(".json"):
        with open(config_file, "r") as f:
            keywords = json.load(f)
    else:
        raise ValueError("Invalid configuration file format")

    with set_directory(Path(config_file).parent):
        restrain_solutes = True
        old_keywords = keywords.copy()
        massage_keywords(keywords, restrain_solutes)

        do_mintherm(keywords, logger)
        do_lambda_annealing(keywords, logger)

        # reestablish the restrained atoms
        if restrain_solutes:
            keywords["POS_RESTRAINED_ATOMS"] = old_keywords.get("POS_RESTRAINED_ATOMS")

        do_equil(keywords, logger)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Specify ONE input file"

    rbfe_structprep(sys.argv[1])
