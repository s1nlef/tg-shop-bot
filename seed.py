import asyncio
from app.database.models import async_session, Sneaker, SneakerSize
from sqlalchemy import select


async def clear_database():
    """Очистка таблиц перед заполнением (опционально)"""
    async with async_session() as session:
        # Удаляем все размеры и кроссовки
        await session.execute(select(SneakerSize).delete())
        await session.execute(select(Sneaker).delete())
        await session.commit()
        print("✅ База данных очищена")


async def seed_sneakers():
    """Заполнение базы данных кроссовками из brands.txt"""

    sneakers_data = [
        # Nike
        {
            "brand": "Nike",
            "model": "Air Jordan 3",
            "colorway": "World's Best",
            "price": 215,
            "image_url": "https://static.nike.com/a/images/t_web_pdp_535_v2/f_auto,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/245d9c12-04ad-4ec2-bd98-9ae53337956a/AIR+JORDAN+3+RETRO+OG.png",
            "sizes": {"39": 5, "40": 7, "41": 8, "42": 6, "43": 4, "44": 3, "45": 2},
        },
        {
            "brand": "Nike",
            "model": "Air Jordan 1 Retro High OG",
            "colorway": "Flight Club",
            "price": 185,
            "image_url": "https://static.nike.com/a/images/t_web_pdp_535_v2/f_auto,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/8a154076-d2fd-491c-adb5-518345572a92/AIR+JORDAN+1+RETRO+HIGH+OG+FC.png",
            "sizes": {"39": 6, "40": 8, "41": 9, "42": 7, "43": 5, "44": 4, "45": 3},
        },
        {
            "brand": "Nike",
            "model": "Jordan Son of Mars Low",
            "colorway": "Color",
            "price": 165,
            "image_url": "https://static.nike.com/a/images/t_web_pdp_535_v2/f_auto,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/9c496858-ea88-47b4-8038-b54862453bbd/JORDAN+SON+OF+MARS+LOW.png",
            "sizes": {"39": 4, "40": 5, "41": 7, "42": 6, "43": 5, "44": 3, "45": 2},
        },
        {
            "brand": "Nike",
            "model": "Air Jordan 4 Retro",
            "colorway": "Flight Club",
            "price": 220,
            "image_url": "https://static.nike.com/a/images/t_web_pdp_535_v2/f_auto,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/e7ca4c33-67d7-4dc1-95cc-af8313396199/AIR+JORDAN+4+RETRO+OG+FC.png",
            "sizes": {
                "39": 5,
                "40": 6,
                "41": 8,
                "42": 7,
                "43": 6,
                "44": 5,
                "45": 4,
                "46": 3,
            },
        },
        # Asics
        {
            "brand": "Asics",
            "model": "EARLS x GEL-CUMULUS 16",
            "colorway": "Coconut Milk/Black",
            "price": 180,
            "image_url": "https://images.asics.com/is/image/asics/1203B053_200_SB_FR_GLB?$zoom$",
            "sizes": {"39": 4, "40": 5, "41": 7, "42": 6, "43": 5, "44": 4, "45": 3},
        },
        {
            "brand": "Asics",
            "model": "GEL-NIMBUS 28",
            "colorway": "Black/Feather Grey",
            "price": 170,
            "image_url": "https://images.asics.com/is/image/asics/1011C127_002_SB_FR_GLB?$zoom$",
            "sizes": {
                "39": 5,
                "40": 6,
                "41": 8,
                "42": 7,
                "43": 6,
                "44": 5,
                "45": 4,
                "46": 3,
            },
        },
        {
            "brand": "Asics",
            "model": "GEL-KAYANO 12.1",
            "colorway": "Cream/Carbon",
            "price": 170,
            "image_url": "https://images.asics.com/is/image/asics/1203A759_105_SB_FR_GLB?$zoom$",
            "sizes": {"39": 5, "40": 6, "41": 8, "42": 7, "43": 6, "44": 5, "45": 4},
        },
        {
            "brand": "Asics",
            "model": "GEL-RESOLUTION 5",
            "colorway": "Cream/Clay Grey",
            "price": 150,
            "image_url": "https://images.asics.com/is/image/asics/1203A901_100_SB_FR_GLB?$zoom$",
            "sizes": {"39": 4, "40": 5, "41": 7, "42": 6, "43": 5, "44": 4, "45": 3},
        },
        {
            "brand": "Asics",
            "model": "GEL-KINETIC 2.0",
            "colorway": "Pure Silver/Blue Coast",
            "price": 250,
            "image_url": "https://images.asics.com/is/image/asics/1203A678_022_SB_FR_GLB?$zoom$",
            "sizes": {
                "39": 4,
                "40": 5,
                "41": 7,
                "42": 6,
                "43": 5,
                "44": 4,
                "45": 3,
                "46": 2,
            },
        },
        # New Balance
        {
            "brand": "New Balance",
            "model": "530",
            "colorway": "Red",
            "price": 110,
            "image_url": "https://nb.scene7.com/is/image/NB/u530178_nb_05_i?$dw_detail_main_lg$&bgc=f1f1f1&layer=1&bgcolor=f1f1f1&blendMode=mult&scale=10&wid=1600&hei=1600",
            "sizes": {
                "39": 6,
                "40": 7,
                "41": 9,
                "42": 8,
                "43": 7,
                "44": 6,
                "45": 5,
                "46": 4,
            },
        },
        {
            "brand": "New Balance",
            "model": "Made in USA 990v6",
            "colorway": "Grey with WHITE",
            "price": 200,
            "image_url": "https://nb.scene7.com/is/image/NB/m990gl6_nb_05_i?$dw_detail_main_lg$&bgc=f1f1f1&layer=1&bgcolor=f1f1f1&blendMode=mult&scale=10&wid=1600&hei=1600",
            "sizes": {
                "39": 6,
                "40": 7,
                "41": 9,
                "42": 8,
                "43": 7,
                "44": 6,
                "45": 5,
                "46": 4,
            },
        },
        {
            "brand": "New Balance",
            "model": "P350",
            "colorway": "BLACK with FADED BLACK",
            "price": 110,
            "image_url": "https://nb.scene7.com/is/image/NB/uhsl4x0_nb_05_i?$dw_detail_main_lg$&bgc=f1f1f1&layer=1&bgcolor=f1f1f1&blendMode=mult&scale=10&wid=1600&hei=1600",
            "sizes": {"39": 5, "40": 6, "41": 7, "42": 6, "43": 5, "44": 4, "45": 3},
        },
        {
            "brand": "New Balance",
            "model": "Made in USA 992 Core",
            "colorway": "Grey with GREY 006 and WHITE",
            "price": 200,
            "image_url": "https://nb.scene7.com/is/image/NB/u992gy_nb_02_i?$dw_detail_main_lg$&bgc=f1f1f1&layer=1&bgcolor=f1f1f1&blendMode=mult&scale=10&wid=1600&hei=1600",
            "sizes": {
                "39": 5,
                "40": 6,
                "41": 8,
                "42": 7,
                "43": 6,
                "44": 5,
                "45": 4,
                "46": 3,
            },
        },
        {
            "brand": "New Balance",
            "model": "NB Numeric Jamie Foy 306 Cup",
            "colorway": "WHITE with BLACK",
            "price": 95,
            "image_url": "https://nb.scene7.com/is/image/NB/un306cgi_nb_05_i?$dw_detail_main_lg$&bgc=f1f1f1&layer=1&bgcolor=f1f1f1&blendMode=mult&scale=10&wid=1600&hei=1600",
            "sizes": {"39": 5, "40": 6, "41": 8, "42": 7, "43": 6, "44": 5, "45": 4},
        },
    ]

    async with async_session() as session:
        for sneaker_data in sneakers_data:
            # Создаем кроссовок
            sneaker = Sneaker(
                brand=sneaker_data["brand"],
                model=sneaker_data["model"],
                colorway=sneaker_data["colorway"],
                price=sneaker_data["price"],
                image_url=sneaker_data["image_url"],
            )
            session.add(sneaker)
            await session.flush()  # Получаем ID кроссовка

            # Добавляем размеры
            for size, stock in sneaker_data["sizes"].items():
                sneaker_size = SneakerSize(
                    sneaker_id=sneaker.id, size=size, stock=stock
                )
                session.add(sneaker_size)

            print(
                f"✅ Добавлен: {sneaker.brand} {sneaker.model} ({len(sneaker_data['sizes'])} размеров)"
            )

        await session.commit()
        print(f"\n🎉 Всего добавлено кроссовок: {len(sneakers_data)}")


async def main():
    print("🚀 Запуск seed.py...")
    print("⚠️  Внимание: существующие данные будут удалены!\n")

    # Раскомментируйте следующую строку, если хотите очистить БД перед заполнением
    # await clear_database()

    await seed_sneakers()
    print("\n✅ Заполнение базы данных завершено!")


if __name__ == "__main__":
    asyncio.run(main())
