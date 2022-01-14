import pytest
import pandas as pd
from splicing_outlier_prediction import SpliceOutlierDataloader, SpliceOutlier, CatInference

vcf_file = 'tests/data/test.vcf.gz'
multi_vcf_file = 'tests/data/multi_test.vcf.gz'
multi_vcf_samples = 'tests/data/multi_test.vcf_samples.csv'
fasta_file = 'tests/data/hg19.nochr.chr17.fa'
gene_mapping = 'tests/data/gene_mapping_hg19.tsv'
gene_tissue_tpm = 'tests/data/gene_tissue_tpm.csv'

# ref_table5_kn_testis = 'tests/data/test_testis_ref_table5_kn.csv'
# ref_table3_kn_testis = 'tests/data/test_testis_ref_table3_kn.csv'
# ref_table5_kn_lung = 'tests/data/test_lung_ref_table5_kn.csv'
# ref_table3_kn_lung = 'tests/data/test_lung_ref_table3_kn.csv'
# ref_table5_kn_blood = 'tests/data/test_blood_ref_table5_kn.csv'
# ref_table3_kn_blood = 'tests/data/test_blood_ref_table3_kn.csv'
ref_table5_kn_testis = 'tests/data/Testis_splicemap_psi5_method=kn_event_filter=median_cutoff.csv'
ref_table3_kn_testis = 'tests/data/Testis_splicemap_psi3_method=kn_event_filter=median_cutoff.csv'
ref_table5_kn_lung = 'tests/data/Lung_splicemap_psi5_method=kn_event_filter=median_cutoff.csv'
ref_table3_kn_lung = 'tests/data/Lung_splicemap_psi3_method=kn_event_filter=median_cutoff.csv'
ref_table5_kn_blood = 'tests/data/Cells_Cultured_fibroblasts_splicemap_psi5_method=kn_event_filter=median_cutoff.csv'
ref_table3_kn_blood = 'tests/data/Cells_Cultured_fibroblasts_splicemap_psi3_method=kn_event_filter=median_cutoff.csv'

combined_ref_tables5_testis_lung = 'tests/data/test_combined_ref_tables5_testis_lung_kn.csv'
combined_ref_tables3_testis_lung = 'tests/data/test_combined_ref_tables3_testis_lung_kn.csv'

count_cat_file_lymphocytes_complete = 'tests/data/create_test/data/full_data/backup/test_count_table_cat_chrom17_lymphocytes.csv'
count_cat_file_blood_complete = 'tests/data/create_test/data/full_data/backup/test_count_table_cat_chrom17_blood.csv'
count_cat_file_lymphocytes = 'tests/data/test_count_table_cat_chrom17_lymphocytes.csv'
count_cat_file_blood = 'tests/data/test_count_table_cat_chrom17_blood.csv'

mmsplice_path = 'tests/data/test_mmsplice.csv'
spliceai_path = 'tests/data/test_spliceAI.csv'
mmsplice_cat_path = 'tests/data/test_mmsplice_cat.csv'
pickle_DNA = 'tests/data/model_DNA_trained_on_all_GTEx.pkl'
pickle_DNA_CAT = 'tests/data/model_CAT_concat.pkl'

pickle_absplice_DNA = 'tests/data/AbSplice_DNA_trained_on_all_GTEx.pkl'
pickle_absplice_RNA = 'tests/data/AbSplice_RNA_trained_on_all_GTEx.pkl'

@pytest.fixture
def var_samples_df():
    return pd.read_csv(multi_vcf_samples)

@pytest.fixture
def outlier_dl():
    return SpliceOutlierDataloader(
        fasta_file, vcf_file,
        splicemap5=[ref_table5_kn_testis, ref_table5_kn_lung],
        splicemap3=[ref_table3_kn_testis, ref_table3_kn_lung])


@pytest.fixture
def cat_dl():
    return [
        CatInference(splicemap5=[ref_table5_kn_testis, ref_table5_kn_lung],
                     splicemap3=[ref_table3_kn_testis, ref_table3_kn_lung],
                     count_cat=count_cat_file_lymphocytes,
                     name='lymphocytes'),
        CatInference(splicemap5=[ref_table5_kn_testis, ref_table5_kn_lung],
                     splicemap3=[ref_table3_kn_testis, ref_table3_kn_lung],
                     count_cat=count_cat_file_blood,
                     name='blood'),
    ]


@pytest.fixture
def outlier_model():
    return SpliceOutlier()


@pytest.fixture
def outlier_results(outlier_model, outlier_dl):
    return outlier_model.predict_on_dataloader(outlier_dl)


@pytest.fixture
def outlier_results_multi(outlier_model, outlier_dl_multi, var_samples_df):
    results = outlier_model.predict_on_dataloader(outlier_dl_multi)
    results.add_samples(var_samples_df)
    return results


@pytest.fixture
def outlier_dl_multi():
    return SpliceOutlierDataloader(
        fasta_file, multi_vcf_file,
        splicemap5=[ref_table5_kn_testis, ref_table5_kn_lung],
        splicemap3=[ref_table3_kn_testis, ref_table3_kn_lung]
    )
    
    
    
@pytest.fixture
def mmsplice_splicemap_cols():
    return sorted([
        'variant', 'junction', 'tissue', 'event_type',
        'Chromosome', 'Start', 'End', 'Strand',
        'events', 'splice_site', 'ref_psi', 'k', 'n', 'median_n',
        'novel_junction', 'weak_site_donor', 'weak_site_acceptor',
        'gene_id', 'gene_name', 'transcript_id', 'gene_type', 'gene_tpm',
        'delta_logit_psi', 'delta_psi',
        'ref_acceptorIntron', 'ref_acceptor', 'ref_exon', 'ref_donor', 'ref_donorIntron',
        'alt_acceptorIntron', 'alt_acceptor', 'alt_exon', 'alt_donor', 'alt_donorIntron'])
    
    
@pytest.fixture
def gene_map():
    return pd.read_csv(gene_mapping, sep='\t')

@pytest.fixture
def gene_tpm():
    return pd.read_csv(gene_tissue_tpm)
     
