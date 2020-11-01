create table if not exists new_inserts_re_ownership
(
	new_id int not null,
	insertion_time text not null
);

create or replace function catch_insertion()
returns trigger as
$example_table$
   begin
      insert into new_inserts_re_ownership(new_id, insertion_time) values (new.id, current_timestamp);
      return new;
   end;
$example_table$ language plpgsql;

create trigger re_ownership_insert_control
	after insert on re_ownership
	for each row
	execute procedure catch_insertion()
	