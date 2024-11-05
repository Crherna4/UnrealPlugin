from unreal import (
    AssetToolsHelpers,
    AssetTools,
    EditorAssetLibrary,
    Material,
    MaterialFactoryNew,
    MaterialProperty,
    MaterialEditingLibrary,
    MaterialExpressionTextureSampleParameter2D as TexSample2D,
    AssetImportTask,
    FbxImportUI
)

# Importing necessary Unreal Engine modules for asset manipulation and material editing

import os  # Importing Python's os module for file path operations

# Define a utility class for Unreal Engine
class UnrealUtility:
    def __init__(self):
        # Set base directories and asset names
        self.stubstanceRootDir = "/game/Substance/"
        self.baseMaterialName = "M_SubstanceBase"
        self.substanceTempDir = "/game/Substance/Temp/"
        # Full path to the base material
        self.baseMaterialPath = self.stubstanceRootDir + self.baseMaterialName
        # Names for the material parameters
        self.baseColorName = "BaseColor"
        self.normalName = "Normal"
        self.occRoughnessMetalicName = "OcclusionRoughnessMetalic"

    # Method to find or create a base material in Unreal
    def FindOrCreateBaseMaterial(self):
        # Check if the base material already exists
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath):
            # If it exists, load and return it
            return EditorAssetLibrary.load_asset(self.baseMaterialPath)
        
        # If not, create a new material asset
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.baseMaterialName, self.stubstanceRootDir, Material, MaterialFactoryNew())

        # Create a texture sample parameter for base color
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0)
        baseColor.set_editor_property("parameter_name", self.baseColorName)
        # Connect the base color parameter to the material's base color property
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)

        # Create a texture sample parameter for the normal map
        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)
        normal.set_editor_property("parameter_name", self.normalName)
        # Load a default normal texture and set it as the texture
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        # Connect the normal parameter to the material's normal property
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)

        # Create a texture sample parameter for occlusion, roughness, and metallic maps
        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800)
        occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetalicName)
        # Connect each channel to its respective property in the material
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC)

        # Save the newly created material asset
        EditorAssetLibrary.save_asset(baseMat.get_path_name())
        return baseMat  # Return the base material

    # Method to load a mesh from a given file path
    def LoadMeshFromPath(self, meshPath):
        # Extract the mesh name by removing the directory and extension
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "")
        # Create an import task for the mesh
        importTask = AssetImportTask()
        importTask.replace_existing = True  # Replace any existing asset with the same name
        importTask.filename = meshPath  # Set the mesh file path
        importTask.destination_path = "/game/" + meshName  # Set the destination path in the game directory
        importTask.save = True  # Save the imported mesh asset
        importTask.automated = True  # Automate the import

        # Set import options for the FBX file
        fbxImportOptions = FbxImportUI()
        fbxImportOptions.import_mesh = True  # Enable mesh import
        fbxImportOptions.import_as_skeletal = False  # Import as static mesh (not skeletal)
        fbxImportOptions.import_materials = False  # Disable material import
        fbxImportOptions.static_mesh_import_data.combine_meshes = True  # Combine meshes into a single asset
        
        importTask.options = fbxImportOptions  # Assign the import options to the task

        # Execute the import task
        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask])
        return importTask.get_objects()  # Return the imported objects

    # Method to load all meshes from a directory
    def LoadFromDir(self, fileDir):
        # Loop through all files in the given directory
        for file in os.listdir(fileDir):
            # If the file has an ".fbx" extension, load it as a mesh
            if ".fbx" in file:
                self.LoadMeshFromPath(os.path.join(fileDir, file))
