from re import fullmatch


def get_search_type(serch_term):
    date_pattern=r'^\d{4}-\d{2}-\d{2}$'
    if fullmatch(date_pattern, serch_term):
        return 'date'
    return 'text'


def get_df_result_by_date(metadata_df, date):
    return metadata_df.loc[metadata_df['publish_time'] == date]


def get_df_result_by_text(metadata_df, text):
    # TODO Use threads to process the search in each column
    metadata_df['search_title_score'] = metadata_df['title'].str.lower().str.count(text)
    metadata_df['search_journal_score'] = metadata_df['journal'].str.lower().str.count(text)
    metadata_df['search_authors_score'] = metadata_df['authors'].str.lower().str.count(text)
    metadata_df['search_abstract_score'] = metadata_df['abstract'].str.lower().str.count(text)

    metadata_df['search_score'] = (metadata_df['search_title_score'].fillna(0) + metadata_df['search_journal_score'].fillna(0)
        + metadata_df['search_authors_score'].fillna(0) + metadata_df['search_abstract_score'].fillna(0))
    
    sorted_result = metadata_df.sort_values(by=['search_score'], ascending=False)

    return sorted_result.loc[sorted_result['search_score'] > 0]


def get_df_search_result(metadata_df, search_term):
    if get_search_type(search_term) == 'date':
        return get_df_result_by_date(metadata_df, search_term)
    
    return get_df_result_by_text(metadata_df, search_term)
