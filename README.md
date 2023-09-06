# AaC-BOM
An Architecture-as-Code (AaC) 3rd party plugin for defining and managing your system's Bill of Materials (BOM).

## Motivation
When designing a system of any reasonable scale you have to define and price material for that system. This often includes creating named "things" and establishing the parts the make up that "thing".  Then "things" are aggregated, assigned to locations with need dates, and sent over to a supply chain management team for review and formalization in the business systems.  One challenge is that this often becomes an iterative process and is expected to be done using the supply chain listing rather than the more descriptive engineering data.  The AaC-BOM plugin attempts to provide a way to capture the engineering data in a manner than can be rigorously CM'ed and iteratively updated.  The gen-bom command generates a csv table of the material than can be provided to program management and supply chain staff in a familiar format (i.e. easily pulled into MS Excel). So next time you're given the "cut 10% of material costs" instructions, you can do it in the context of an engineering model of the system with the descriptive information to help you minimize unintentional errors along the way.  You can also more easily evaluate the impact of changes made to the material plan over time.  And hopefully if the baseline is properly CM'ed with appropriate transparency, the team will always have an authoratitive source of what material is actually in the plan.

## Defining a Material Model
There are 3 key elements of a material model:  Site, Assembly, and Part.

- Site:  This defines a location where material will be delivered / deployed.  Sites can be nested, allowing the modeler to define something like "campus -> building -> room" within their site model as needed.  Sites can contain sub-sites, assemblies, and parts.
- Assembly:  This defines a logical collection of "things".  Assemblies can be nested, allowing the modeler to define something like "car -> engine -> cooling" within their assembly model as needed.  Assemblies contain sub-assemblies and parts.
- Part:  This is a material unit used to define an explicit "thing".  The thing should be clearly definable in a manner that would support procurement.

## Using a Material Model
There are 2 validators and 1 command provided to support working with your material model.

### Validators

- No Circular References: When defining site/sub-site or assembly/sub-assembly constructs, it is important to ensure a child object does not reference a parent...creating an infinite loop of material definitions.
- Referenced Material Exists:  Whether referencing a sub-site, assembly, sub-assembly, or part, it is important that the referenced item exists to avoid "holes" in the material model.

### Commands

- Generate BOM:  Validates and analyzes the material model, creating a "fan out" of all defined sites, assemblies, and parts to create a comma separated value (CSV) file that can be easily imported into MS Excel for further manipulation or formatting.  Each row represents a part to procure for a particular site per the model.  The need date for each defined line is taken from the "lowest" site or assembly in the model heirarchy, overriding any "higher" definitions.
  - usage:  aac gen-bom <material_model_file> <output_directory>

## Future
It may be valuable to provide additional commands to help streamline material modeling.  Here are some candidates:
- Total Cost:  Provides a quick way to evaluate the total cost of material in a model.  This would simply run the gen-bom logic and sum the total cost of each line.  The idea would be to simplify the modeler's workflow when trying to hit a target cost value.  The target cost threshold could also be provided as an optional parameter which would fail if total cost were to exceed the threshold, enabling a simple CI/CD test step to ensure material costs do not grow beyond expectations.
- Material Visualization:  Provides the ability to generate a visualization of the material model.  This could be a series of nested boxes which list the parts defined within each.  Perhaps this could generate a little web site that enables uses to "click through" the visualization and see details of selected sites, assemblies, and parts...or even provide a tree view the user can expand / collapse to help navigate large or complex material models.
- Procurement Status:  It may be valuable to define procurement activities, providing transparency of material availability such as receipt date or expiration (i.e. services / software licenses).
- End of Life / End of Sale:  It may be valuable to capture information on the lifecycle of parts, enabling EOS/EOL analysis and planning.  This could be particularly valuable for IT equipment where security patching is reliant on EOS/EOL dates.
- Sparing:  It may be valuable to enable explicit differentiation of "active vs spare" material.  This could enable analysis related to operational availability or fault recovery estimation.
- Reliability:  It may be valuable to capture reliability information such as part level MTBF or "M-of-N" configurations in redundant configurations.  This would enable overall system reliability analysis based on the characteristics and configuration of constituant parts.