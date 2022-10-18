image:
	docker build -t foehn:latest .

run: image
	docker compose up --remove-orphans

fixtures:
	./manage.py dumpdata \
		-o foehn/fixtures/0001_la_haute_borne.json \
		foehn.Manufacturer \
		foehn.TurbineModel \
		foehn.Organization \
		foehn.Site \
		foehn.Turbine \
		foehn.PowerCurve \
		foehn.ScadaFileFormat

.PHONY: image run