import csv


def search_properties(csv_file, query, search_type):

    matches = []

    query = query.upper()


    with open(
        csv_file,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)


        for row in reader:

            if search_type == "owner":

                fields = [
                    row.get("owner_name_1", ""),
                    row.get("owner_name_2", "")
                ]


            elif search_type == "mailing":

                fields = [
                    row.get("owner_address_1", ""),
                    row.get("owner_address_2", "")
                ]


            elif search_type == "property":

                fields = [
                    row.get("location_house_number", ""),
                    row.get("location_street_direction", ""),
                    row.get("location_street_name", ""),
                    row.get("location_street_suffix", "")
                ]


            else:
                raise ValueError(
                    "Invalid search type"
                )


            searchable = " ".join(fields).upper()


            if query in searchable:

                matches.append(row)


    return matches
