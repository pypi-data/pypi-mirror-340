import pandas as pd
from wormcat3 import file_util

class AnnotationsManager:
    """Manages gene annotations and preprocessing."""
    
    def __init__(self, annotation_file):
        """Initialize with the path to the annotation file."""
        if file_util.is_file_path(annotation_file):
            self.annotation_file_path = annotation_file
        else:
            self.annotation_file_path = file_util.find_file_path(annotation_file)
            if not self.annotation_file_path:
                raise FileNotFoundError(f"Annotation file not found: {annotation_file}")
                        
        self.annotations_df = self._load_annotations()
            
     
        
    def _load_annotations(self):
        """Load annotations from file."""
        try:
            df = pd.read_csv(self.annotation_file_path)
            df.columns = df.columns.str.replace(' ', '.')
            if df.empty:
                raise ValueError(f"Annotation file '{self.annotation_file_path}' is empty.")
            return df
        except Exception as e:
            raise ValueError(f"Failed to load annotation file: {e}")
    
    def get_gene_id_type(self, gene_set):
        """Determine the gene ID type from the gene set."""
        if len(gene_set) < 2:
            raise ValueError("At least two genes are required for comparison.")
        
        # Check if the first two genes start with "WBGene"
        if gene_set[0].startswith("WBGene") and gene_set[1].startswith("WBGene"):
            return "Wormbase.ID"
        elif not gene_set[0].startswith("WBGene") and not gene_set[1].startswith("WBGene"):
            return "Sequence.ID"
        else:
            raise ValueError("Invalid gene data: One gene starts with 'WBGene', but the other does not.")
    
    @staticmethod
    def dedup_list(input_list):
        """Deduplicate a list while preserving order."""
        seen = set()
        deduped_list = []
        for item in input_list:
            if item not in seen:
                deduped_list.append(item)
                seen.add(item)
        return deduped_list
    
    def add_annotations(self, gene_set_list, gene_type):
        """Add annotations to the gene set."""
        gene_set_df = pd.DataFrame(gene_set_list, columns=[gene_type])
        
        # Verify if 'gene_type' is a column in the DataFrame
        if gene_type not in self.annotations_df.columns:
            raise ValueError(f"Column '{gene_type}' not found in the DataFrame.")
        
        return pd.merge(gene_set_df, self.annotations_df, on=gene_type, how='left')


    def split_background_on_annotation_match(self, background_list, gene_type):
        """Split background genes into those with and without annotations."""
        background_df = pd.DataFrame(background_list, columns=[gene_type])
        
        # Check if gene_type is in both dataframes
        if gene_type not in background_df.columns:
            raise ValueError(f"'{gene_type}' not found in background_df.")
        if gene_type not in self.annotations_df.columns:
            raise ValueError(f"'{gene_type}' not found in annotations_df.")
        
        # Perform the left merge
        merged_df = pd.merge(background_df, self.annotations_df, on=gene_type, how='left')
        
        # Split based on presence of annotation (assuming at least one non-key column in annotations_df)
        annotation_columns = [col for col in self.annotations_df.columns if col != gene_type]
        
        background_available_df = merged_df.dropna(subset=annotation_columns)
        background_not_matched_df = merged_df[merged_df[annotation_columns].isnull().all(axis=1)]
        background_not_matched_df = background_not_matched_df[[gene_type]]

        return background_available_df, background_not_matched_df