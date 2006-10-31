# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2006 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Johan Dahlin            <jdahlin@async.com.br>
##

from stoqlib.database.runtime import get_connection, new_transaction
from stoqlib.domain.person import Person
from tests.sync.base import SyncTest

class TestUpdate(SyncTest):
    def testSimple(self):
        self.switch_to_office()
        trans = new_transaction()
        person = Person(name="Test Person", connection=trans)
        trans.commit()

        self.update("shop-computer")

        self.switch_to_shop()
        trans = new_transaction()
        self.failUnless(
            Person.selectOneBy(name="Test Person",
                               connection=new_transaction()))

    def testDuplex(self):
        # Shop
        self.switch_to_shop()
        trans = new_transaction()
        person = Person(name="Person 1", connection=trans)
        trans.commit()

        # Office
        self.switch_to_office()
        trans = new_transaction()
        person = Person(name="Person 2", connection=trans)
        trans.commit()

        self.update("shop-computer")

        self.failUnless(Person.selectOneBy(name="Person 1",
                                           connection=get_connection()))

        # Shop
        self.switch_to_shop()
        self.failUnless(Person.selectOneBy(name="Person 2",
                                           connection=get_connection()))
