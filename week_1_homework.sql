-- Question 3
select
	count(*)
	,
	case
		when trip_distance <= 1 then '1. Up to 1'
		when trip_distance > 1
		and trip_distance <= 3 then '2. Between 1 and 3'
		when trip_distance > 3
		and trip_distance <= 7 then '3. Between 3 and 7'
		when trip_distance > 7
		and trip_distance <= 10 then '4. Between 7 and 10'
		when trip_distance > 10 then '5. Over 10'
	end as trip_mile_range
from
	green_taxi_trips gtt
where
	1 = 1
	and gtt.lpep_pickup_datetime::date between '2019-10-01' and '2019-10-31'
group by
	2;

-- Question 4
select
	lpep_pickup_datetime
		,
	max(trip_distance)
from
	green_taxi_trips gtt
where
	1 = 1
group by
	1
order by
	max(trip_distance) desc
limit 1;

-- Question 5
select
	tz."Zone"
		,
	round(sum(total_amount)::decimal,
	2) total_dolla_dolla_bills
from
	green_taxi_trips gtt
inner join taxi_zones tz
	on
	tz."LocationID" = gtt."PULocationID"
where
	1 = 1
	and gtt.lpep_pickup_datetime::date = '2019-10-18'
group by
	1
order by
	sum(total_amount) desc;



-- Question 6
select
	tz."Zone" pickup_zone
,
	tz1."Zone" dropoff_zone
,
	max(tip_amount) as total_tip_amount
from
	green_taxi_trips gtt
inner join taxi_zones tz
	on
	tz."LocationID" = gtt."PULocationID"
	and tz."Zone" = 'East Harlem North'

inner join taxi_zones tz1
	on
	tz1."LocationID" = gtt."DOLocationID"

where
	1 = 1
	and extract(year from gtt.lpep_pickup_datetime::date) = 2019
	and extract(month from gtt.lpep_pickup_datetime::date) = 10
group by
	1,
	2
order by
	max(tip_amount) desc;
