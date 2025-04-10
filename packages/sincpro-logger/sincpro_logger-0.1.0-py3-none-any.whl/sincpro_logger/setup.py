from sincpro_logger.adapters.hardware_collector import get_hardware_collector
from sincpro_logger.adapters.discord_hardware_notifier import DiscordHardwareNotifier


def pre_init_logger():
    hardware_collector = get_hardware_collector()
    hardware_info = hardware_collector.collect()
    notifier = DiscordHardwareNotifier()
    notifier.send_hardware_info(hardware_info)
