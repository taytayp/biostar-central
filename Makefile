USER=www
SERVER=metabarcode.com

serve: init
	python manage.py runserver

conda:
	conda install --file conf/conda_requirements.txt -y

uwsgi: init
	uwsgi  --ini conf/devel/devel_uwsgi.ini

clean:
	(cd export/local && make clean)

testdata:
	mkdir -p export/local
	(cd export/local && make  all)

delete:
	# Ensure the files that could hold secrets exist.
	touch conf/main/main_secrets.py
	touch conf/test/test_secrets.py
	# Remove the database and old media.
	rm -f export/database/engine.db
	rm -rf export/media/*

reset: delete init jobs

next:
	python manage.py job --next

hello:
	python manage.py analysis --add --json biostar/tools/hello/hello4.hjson  --template biostar/tools/hello/hello4.sh --create_job
	python manage.py analysis --add --json biostar/tools/hello/hello3.hjson  --template biostar/tools/hello/hello3.sh --create_job
	python manage.py analysis --add --json biostar/tools/hello/hello2.hjson  --template biostar/tools/hello/hello2.sh --create_job
	python manage.py analysis --add --json biostar/tools/hello/hello1.hjson  --template biostar/tools/hello/hello1.sh --create_job



jobs:
	python manage.py analysis --add --json biostar/tools/fastqc/fastqc.hjson  --template biostar/tools/fastqc/fastqc.sh --create_job
	python manage.py analysis --add --json biostar/tools/qc/qc.hjson  --template biostar/tools/qc/qc.sh --create_job
	python manage.py analysis --add --json biostar/tools/classify/classify.hjson  --template biostar/tools/classify/classify.sh --create_job
	python manage.py analysis --add --analysis_type admin --id 2  --json biostar/tools/admin/unpack.hjson --template  biostar/tools/admin/unpack.sh --create_job
	python manage.py analysis --add --analysis_type admin --id 2 --json  biostar/tools/admin/copy.hjson --template  biostar/tools/admin/copy.sh --create_job
	python manage.py analysis --add --json biostar/tools/align/align.hjson  --template biostar/tools/align/align.sh --create_job

init:
	python manage.py collectstatic --noinput -v 0
	python manage.py migrate

test:
	python manage.py test

push:
	git commit -am "Update by `whoami` on `date` from `hostname`"
	git push


test_push:test
	git commit -am "Update by `whoami` on `date` from `hostname`"
	git push

deploy_test:
	fab -f conf/fabfile.py -H ${USER}@${SERVER} deploy_test

deploy_main:
	fab -f conf/fabfile.py -H ${USER}@${SERVER} deploy_main

restart_nginx:
	fab -f conf/fabfile.py -H ${USER}@${SERVER} restart_nginx

restart_django:
	fab -f conf/fabfile.py -H ${USER}@${SERVER} restart_uwsgi


deploy_all: deploy_test deploy_main restart_django
