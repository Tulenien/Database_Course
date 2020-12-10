-- Извлечь json фрагмент из json документа

create temp table import(doc json);
copy import from 
'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\tenantsCopy.json';

select *
into temp tbl
from
(
    -- Получить все, что внутри массива
    select p.*
    from import, json_array_elements(doc) p
    limit 1
) imp;

select * from tbl;

-- Извлечь значения конкретных аттрибутов json документа
create temp table import(doc json);
copy import from 
'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\tenantsCopy.json';

select *
into temp tbl
from
(
    -- Получить все, что внутри массива
    select p.*
    from import, json_array_elements(doc) p
) imp;

select json_extract_path(tbl.value, 'info', 'name') 
from tbl;

-- Выполнить проверку существования узла или аттрибута

with recursive get_keys(key, value) as 
(
  select t.key, t.value
  from tbl, json_each(tbl.value) t
  union all
  select t.key, t.value
  from get_keys, json_each
  (
    case 
      when json_typeof(get_keys.value) <> 'object' then '{}' :: json
      else get_keys.value
    end
  ) as t
)
select distinct key
from get_keys
where json_typeof(get_keys.value) <> 'object';