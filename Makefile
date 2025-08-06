ifeq ($(fedora),1)
DIST = fedora-41
else
DIST = centos-stream+epel-9
endif

NAME = python-docx2txt
SRPM = SRPMS/$(NAME)-*.src.rpm

all:	buildsrpm buildrpm clean

clean:
	rm -rf dist BUILD BUILDROOT RPMS SRPMS

buildsrpm:
	python3 setup.py sdist
	rpmbuild -bs -D "_topdir $(PWD)" -D "_sourcedir $(PWD)/dist" $(NAME).spec

buildrpm:
	mock -r $(DIST)-x86_64 --rebuild $(SRPM)