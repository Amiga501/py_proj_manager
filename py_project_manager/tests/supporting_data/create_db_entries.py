# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 13:59:30 2025

@author: brendan

A support file for enabling tests (and supporting development)

"""
# %% Global imports
from collections.abc import Callable


# -----------------------------------------------------------------------------
def create_deathstar_project(
        db_handler: Callable):
    """!
    **Create a baseline project for tests to use (and extend)**
    
    """
    organ = db_handler.create_organisation(
        name="Galactic Empires Inc",
        logo_path="ExampleLogo.png")
    
    darth_vader = db_handler.create_human_resource(
        forename="Darth",
        surname="Vader",
        email="darth.vader@galactic-empires.com",
        division="Sith Lords",
        working_week_hrs=40,
        )
    darth_maul = db_handler.create_human_resource(
        forename="Darth",
        surname="Maul",
        email="darth.maul@galactic-empires.com",
        division="Sith Lords",
        working_week_hrs=40,
        )
    darth_sideous = db_handler.create_human_resource(
        forename="Darth",
        surname="Sideous",
        email="darth.sideous@galactic-empires.com",
        division="Sith Lords",
        working_week_hrs=40,
        )
    
    death_star = death_star_proj = db_handler.create_project(
        name="Death Star",
        code="DS1",
        organisation_id=organ.id,
        description="""The ultimate power in the universe. The power of the 
        force is insignificant, compared to the ability to destroy a planet.
        """,
        )
     
    hyperdrive = db_handler.create_task(
        name="Hyperdrive",
        project_id=death_star_proj.id,
        )
    
    firing_laser = db_handler.create_task(
        name="Firing Laser",
        project_code="DS1",
        )
    
    hyperdrive_motivator = db_handler.create_taskitem(
        name="Hyperdrive motivator",
        duration_hrs=8,
        task_id=hyperdrive.id,
        )
    
    hyperdrive_power_relay = db_handler.create_taskitem(
        name="Hyperdrive power relay",
        duration_hrs=8,
        task_id=hyperdrive.id,
        )
    
    hyperdrive_flux_coupling = db_handler.create_taskitem(
        name="Hyperdrive flux coupling",
        duration_hrs=8,
        task_id=hyperdrive.id,
        )
    
    firing_laser_focussing_crystals = db_handler.create_taskitem(
        name="Firing laser focussing crystals",
        duration_hrs=8,
        task_id=firing_laser.id,
        )
    
    firing_laser_power_coupling = db_handler.create_taskitem(
        name="Firing laser power coupling",
        duration_hrs=8,
        task_id=firing_laser.id,
        )
    
    firing_laser_trigger = db_handler.create_taskitem(
        name="Firing laser trigger",
        duration_hrs=8,
        task_id=firing_laser.id,
        )
    
    hyperdrive_flux_coupling.add_precedent_taskitem_id(
        hyperdrive_power_relay.id)
    hyperdrive_power_relay.add_precedent_taskitem_id(
        hyperdrive_motivator.id)
    firing_laser_power_coupling.add_precedent_taskitem_id(
        hyperdrive_power_relay.id)
    firing_laser_focussing_crystals.add_precedent_taskitem_id(
        firing_laser_power_coupling.id)
    firing_laser_trigger.add_precedent_taskitem_id(
        firing_laser_focussing_crystals.id)
        
    return {
        "organisations": [organ],
        "resources": {"human": [darth_vader,
                                darth_maul,
                                darth_sideous,
                                ],
                      },
        "projects": [death_star,
                     ],
        "tasks": [hyperdrive,
                  firing_laser,
                  ],
        "taskitems": [hyperdrive_motivator,
                      hyperdrive_power_relay,
                      hyperdrive_flux_coupling,
                      firing_laser_focussing_crystals,
                      firing_laser_power_coupling,
                      firing_laser_trigger
                      ],
        }
