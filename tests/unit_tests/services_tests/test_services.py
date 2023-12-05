"""Not implemented yet."""
'''
    async def test_create(self, init) -> None:
        assert await self._db_empty()
        assert await self._cache_empty()
        await self.base_service.create(self.schema(**self.post_payload))
        assert not await self._db_empty()
        assert await self._cache_empty()

    async def test_update(self, get_obj_from_db: d.Model) -> None:
        assert not await self._db_empty()
        assert await self._cache_empty()
        await self.base_service.update(get_obj_from_db.id, self.schema(**self.update_payload))
        assert not await self._db_empty()
        assert await self._cache_empty()

    async def test_delete(self, get_obj_from_db: d.Model) -> None:
        assert not await self._db_empty()
        assert await self._cache_empty()
        await self.base_service.delete(get_obj_from_db.id)
        assert await self._db_empty()
        assert await self._cache_empty()
'''
