
from collections import namedtuple

# An example is Core("first", 1.5, True)
Core = namedtuple("Core", "n length cortex")


def is_cortex_visualized(cores: list[Core]):
    """Takes a list of cores, and returns a list of cores that contain a cortex"""
    cores_with_cortex = [c for c in cores if c.cortex]
    return len(cores_with_cortex) > 0


def scenario_1c(core: Core):
    """Solves a scenario where only one core is retrieved. Takes a core, returns the diagnostic core along with its
    processing instructions"""
    if core.cortex and core.length >= 0.5:
        message = """A minimum of 0.5 cm of cortex needs to be fixed in formalin for LM. 
        A minimum of 0.2 cm needs to be frozen in OCT and processed for IF. 
        0.1 cm cortex needs to be fixed in glutaraldehyde for EM. Prioritize LM > IF > EM."""
    elif core.cortex and core.length < 0.5:
        message = "The entire tissue will be fixed in formalin to be processed for Light Microscopy."
    else:
        message = "The entire tissue will be fixed in formalin to be processed for Light Microscopy."
    return core, message


def scenario_23c_visualized_cortex(cores: list[Core]):
    """Solves a scenario where two or three cores are retrieved and cortex is visualized in at least one core.
    Takes a list of cores, returns the diagnostic core along with its processing instructions
    """
    # to find the diagnostic core, start by eliminating the cores without cortext
    cores = [c for c in cores if c.cortex]
    # then assign the longest core as the diagnostic core
    cores = sorted(cores, key=lambda x: x.length, reverse=True)
    diagnostic_core = cores[0]
    if diagnostic_core.length >= 1.4:
        message = (f"Assign the {diagnostic_core.n} core that is {diagnostic_core.length} cm long as the diagnostic core. "
                   f"If the amount of cortext is less than 0.5 cm then please the entire core in formalin for light microscopy. "
                   f"Otherwise, divide diagnostic core in three parts with a minimum of 0.1-0.2 cm of cortex fixed in 2.5% glutaraldehyde for EM, 0.3 cm cortex frozen in OCT for IF, "
                   f"and the remaining amount of tissue fixed in 10% formalin for LM. \n")
        return diagnostic_core, message + additional_core_instructions(cores)
    else:
        return scenario_23c_small(cores)


def scenario_23c_no_cortex(cores: list[Core]):
    """Solves a scenario where two or three cores are retrieved and cortex is not visualized.
    Takes a list of cores, returns the diagnostic core along with its processing instructions
    """
    # if any of the cores has cortext then throw an error
    if len([c for c in cores if c.cortex]) > 0:
        raise Exception("this function cannot be provided cores with cortext")
    # assign the longest core as the diagnostic core
    cores = sorted(cores, key=lambda x: x.length, reverse=True)
    diagnostic_core = cores[0]
    if diagnostic_core.length >= 1.4:
        message = (f"Assign the {diagnostic_core.n} that is {diagnostic_core.length} cm long core as the diagnostic core. "
                   f"A minimum of 0.1-0.2 cm of tissue from both tips of the diagnostic core should be placed in glutaraldehyde for EM, "
                   f"a 0.3 cm of tissue from both tips will be frozen in OCT for IF, and the remaining tissue will be placed in formalin for LM. \n")
        return diagnostic_core, message + additional_core_instructions(cores)
    else:
        return scenario_23c_small(cores)


def scenario_23c_small(cores: list[Core]):
    """Solves a scenario where two or three cores are retrieved but all of them are smaller than 1.4 cm of length.
    Takes a list of cores, returns the diagnostic core along with its processing instructions
    """
    message = """All biopsy cores are less than 1.4 cm. A minimum of 0.5 cm of cortex needs to be placed into formalin for LM. 
    A minimum of 0.2 cm cortex needs to be frozen in OCT to be processed for IF. A minimum of 0.1 cm cortex needs to be placed in glutaraldehyde for EM. 
    In the event of scarce tissue availability, prioritize LM > IF > EM. \n"""
    return message + additional_core_instructions(cores)


def additional_core_instructions(cores: list[Core]):
    """Takes a list of cores, and returns the instructions to process the non-diagnostic cores"""
    if len(cores) == 3:
        other_message = "The remaining two cores will be designated for tissue interrogation and triaged/processed as cores #2 and #3."
    elif len(cores) == 2:
        other_message = "The second biopsy core should be embedded in OCT, frozen on dry ice and shipped to the central bio-repository where it will be distributed to the TISs."
    else:
        other_message = ""
    return other_message


def triage_biopsy(
    core1_length: float = 0,
    core1_cortex: bool = False,
    core2_length: float = 0,
    core2_cortex: bool = False,
    core3_length: float = 0,
    core3_cortex: bool = False,
):
    """Triages a biopsy in KPMP study"""
    n_cores = (core1_length > 0) + (core2_length > 0) + (core3_length > 0)
    if n_cores == 1:
        return scenario_1c(Core("first", core1_length, core1_cortex))
    elif n_cores == 2:
        core1 = Core("first", core1_length, core1_cortex)
        core2 = Core("second", core2_length, core2_cortex)
        cores = [core1, core2]
    elif n_cores == 3:
        core1 = Core("first", core1_length, core1_cortex)
        core2 = Core("second", core2_length, core2_cortex)
        core3 = Core("third", core3_length, core3_cortex)
        cores = [core1, core2, core3]
    else:
            return "You can perform up to 5 passes to obtain more cores."

    if is_cortex_visualized(cores):
        return scenario_23c_visualized_cortex(cores)
    else:
        return scenario_23c_no_cortex(cores)


if __name__ == "__main__":
    print(triage_biopsy(1.5, True, 1.2, False, 0.5, True))
