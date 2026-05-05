-- Supabase/PostgreSQL schema for Miralyze.
-- Execute this script once from the Supabase SQL editor.

create table if not exists companies (
    id bigserial primary key,
    company_name text not null,
    cif text,
    bvd_id text,
    date_of_establishment date,
    website text,
    country text,
    province text,
    guo_name text,
    cnae_code text not null,
    native_trade_description text,
    english_trade_description text,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

create unique index if not exists idx_companies_bvd_id
    on companies (bvd_id) where bvd_id is not null and bvd_id <> '';
create index if not exists idx_companies_name on companies (company_name);
create index if not exists idx_companies_cif on companies (cif);
create index if not exists idx_companies_cnae on companies (cnae_code);
create index if not exists idx_companies_country on companies (country);
create index if not exists idx_companies_province on companies (province);

create table if not exists financials (
    id bigserial primary key,
    company_id bigint not null references companies(id) on delete cascade,
    year integer not null,
    cash_and_equivalents numeric,
    total_assets numeric,
    working_capital numeric,
    employees integer,
    revenue numeric,
    cost_of_goods_sold numeric,
    ebitda numeric,
    long_term_debts numeric,
    short_term_debts numeric,
    equity numeric,
    net_income numeric,
    cash_flow numeric,
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    unique (company_id, year)
);

create index if not exists idx_financials_company on financials(company_id);
create index if not exists idx_financials_year on financials(year);

create table if not exists metrics (
    id bigserial primary key,
    company_id bigint not null references companies(id) on delete cascade,
    year integer not null,
    gross_debt numeric,
    net_debt numeric,
    ebitda_margin numeric,
    net_income_margin numeric,
    cash_flow_margin numeric,
    revenue_growth_yoy numeric,
    ebitda_growth_yoy numeric,
    revenue_cagr_3y numeric,
    revenue_cagr_5y numeric,
    net_debt_ebitda numeric,
    revenue_per_employee numeric,
    ebitda_per_employee numeric,
    cash_flow_per_employee numeric,
    cash_conversion numeric,
    equity_ratio numeric,
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    unique (company_id, year)
);

create index if not exists idx_metrics_company on metrics(company_id);
create index if not exists idx_metrics_year on metrics(year);

create table if not exists import_log (
    id bigserial primary key,
    import_timestamp timestamptz default now(),
    file_name text,
    file_type text,
    load_mode text,
    rows_read integer,
    rows_accepted integer,
    rows_rejected integer,
    notes text
);

create table if not exists import_errors (
    id bigserial primary key,
    import_id bigint not null references import_log(id) on delete cascade,
    row_number integer,
    error_type text,
    error_description text
);

create or replace function set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_companies_updated_at on companies;
create trigger trg_companies_updated_at
before update on companies
for each row execute function set_updated_at();

drop trigger if exists trg_financials_updated_at on financials;
create trigger trg_financials_updated_at
before update on financials
for each row execute function set_updated_at();

drop trigger if exists trg_metrics_updated_at on metrics;
create trigger trg_metrics_updated_at
before update on metrics
for each row execute function set_updated_at();
